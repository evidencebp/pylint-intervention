from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, datetime, timedelta
from io import StringIO
import logging
import pytz
from typing import Collection, List

from sqlalchemy.orm import Session

from rdr_service.dao.consent_dao import ConsentDao
from rdr_service.dao.hpo_dao import HPODao
from rdr_service.dao.participant_summary_dao import ParticipantSummaryDao
from rdr_service.model.consent_file import ConsentFile as ParsingResult, ConsentSyncStatus, ConsentType,\
    ConsentOtherErrors
from rdr_service.model.consent_response import ConsentResponse
from rdr_service.model.participant_summary import ParticipantSummary
from rdr_service.participant_enums import ParticipantCohort, QuestionnaireStatus
from rdr_service.resource.tasks import dispatch_rebuild_consent_metrics_tasks, dispatch_check_consent_errors_task
from rdr_service.services.consent import files
from rdr_service.storage import GoogleCloudStorageProvider


class ValidationOutputStrategy(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process_results()

    def add_all(self, result_collection: Collection[ParsingResult]):
        for result in result_collection:
            self.add_result(result)

    @abstractmethod
    def add_result(self, result: ParsingResult):
        ...

    @abstractmethod
    def process_results(self):
        ...

    @classmethod
    def _build_consent_list_structure(cls):
        def participant_results():
            return defaultdict(lambda: [])
        return defaultdict(participant_results)


class StoreResultStrategy(ValidationOutputStrategy):
    def __init__(self, session, consent_dao: ConsentDao, project_id=None):
        self._session = session
        self._results = []
        self._consent_dao = consent_dao
        self._max_batch_count = 500
        self.project_id = project_id

    def add_result(self, result: ParsingResult):
        self._results.append(result)
        if len(self._results) > self._max_batch_count:
            self.process_results()
            self._results = []

    def _get_existing_results_for_participants(self):
        return self._consent_dao.get_validation_results_for_participants(
            session=self._session,
            participant_ids={result.participant_id for result in self._results}
        )

    @classmethod
    def _file_in_collection(cls, file, collection):
        return any([file.file_path == possible_matching_file.file_path for possible_matching_file in collection])

    def process_results(self):
        previous_results = self._get_existing_results_for_participants()
        new_results_to_store = _ValidationOutputHelper.get_new_validation_results(
            existing_results=previous_results,
            results_to_filter=self._results
        )
        self._consent_dao.batch_update_consent_files(new_results_to_store, self._session)
        self._session.commit()
        if new_results_to_store:
            dispatch_rebuild_consent_metrics_tasks([r.id for r in new_results_to_store], project_id=self.project_id)


class ReplacementStoringStrategy(ValidationOutputStrategy):
    def __init__(self, session, consent_dao: ConsentDao, project_id=None):
        self.session = session
        self.consent_dao = consent_dao
        self.participant_ids = set()
        self.results = self._build_consent_list_structure()
        self._max_batch_count = 500
        self.project_id = project_id

    def add_result(self, result: ParsingResult):
        self.results[result.participant_id][result.type].append(result)
        self.participant_ids.add(result.participant_id)

        if len(self.participant_ids) > self._max_batch_count:
            self.process_results()
            self.results = self._build_consent_list_structure()
            self.participant_ids = set()

    def _build_previous_result_map(self):
        results = self._build_consent_list_structure()
        previous_results = self.consent_dao.get_validation_results_for_participants(
            session=self.session,
            participant_ids=self.participant_ids
        )
        for result in previous_results:
            results[result.participant_id][result.type].append(result)

        return results

    def process_results(self):
        organized_previous_results = self._build_previous_result_map()

        results_to_update = []
        for participant_id, consent_type_dict in self.results.items():
            for consent_type, result_list in consent_type_dict.items():
                previous_type_list: Collection[ParsingResult] = organized_previous_results[participant_id][consent_type]
                new_results = _ValidationOutputHelper.get_new_validation_results(
                    existing_results=previous_type_list,
                    results_to_filter=result_list
                )

                if new_results:
                    ready_for_sync = self._find_file_ready_for_sync(result_list)
                    if ready_for_sync:
                        for result in previous_type_list:
                            if result.sync_status == ConsentSyncStatus.NEEDS_CORRECTING:
                                result.sync_status = ConsentSyncStatus.OBSOLETE
                                results_to_update.append(result)
                        results_to_update.append(ready_for_sync)
                    else:
                        results_to_update.extend(new_results)

        self.consent_dao.batch_update_consent_files(results_to_update, self.session)
        self.session.commit()
        if results_to_update:
            dispatch_rebuild_consent_metrics_tasks([r.id for r in results_to_update], project_id=self.project_id)

    @classmethod
    def _find_file_ready_for_sync(cls, results: List[ParsingResult]):
        for result in results:
            if result.sync_status == ConsentSyncStatus.READY_FOR_SYNC:
                return result

        return None


class UpdateResultStrategy(ReplacementStoringStrategy):
    def _get_existing_results_for_participants(self):
        file_path_list = [file.file_path for file in self.results]
        file_objects: List[ParsingResult] = self.session.query(ParsingResult).filter(
            ParsingResult.file_path.in_(file_path_list)
        ).all()

        return {file.file_path: file for file in file_objects}

    def process_results(self):
        organized_previous_results = self._build_previous_result_map()

        results_to_build = []
        for participant_id, consent_type_dict in self.results.items():
            for consent_type, result_list in consent_type_dict.items():
                previous_type_list: Collection[ParsingResult] = organized_previous_results[participant_id][consent_type]
                # Set the last_checked time for all the matching validation results
                for previous_result in previous_type_list:
                    previous_result.last_checked = datetime.utcnow()

                ready_for_sync = self._find_file_ready_for_sync(result_list)
                if ready_for_sync:
                    found_in_previous_results = False
                    for previous_result in previous_type_list:
                        if previous_result.file_path == ready_for_sync.file_path:
                            self._update_record(new_result=ready_for_sync, existing_result=previous_result)
                            results_to_build.append(previous_result)
                            found_in_previous_results = True
                        elif previous_result.sync_status == ConsentSyncStatus.NEEDS_CORRECTING:
                            previous_result.sync_status = ConsentSyncStatus.OBSOLETE
                            results_to_build.append(previous_result)

                    if not found_in_previous_results:
                        results_to_build.append(ready_for_sync)
                        self.session.add(ready_for_sync)

        self.session.commit()

        if results_to_build:
            dispatch_rebuild_consent_metrics_tasks([r.id for r in results_to_build], project_id=self.project_id)

    @classmethod
    def _update_record(cls, new_result: ParsingResult, existing_result: ParsingResult):
        existing_result.file_exists = new_result.file_exists
        existing_result.type = new_result.type
        existing_result.is_signature_valid = new_result.is_signature_valid
        existing_result.is_signing_date_valid = new_result.is_signing_date_valid

        existing_result.signature_str = new_result.signature_str
        existing_result.is_signature_image = new_result.is_signature_image
        existing_result.signing_date = new_result.signing_date
        existing_result.expected_sign_date = new_result.expected_sign_date

        existing_result.file_upload_time = new_result.file_upload_time
        existing_result.other_errors = new_result.other_errors
        if existing_result.sync_status != ConsentSyncStatus.SYNC_COMPLETE \
                or new_result.sync_status == ConsentSyncStatus.NEEDS_CORRECTING:
            existing_result.sync_status = new_result.sync_status


class LogResultStrategy(ValidationOutputStrategy):
    def __init__(self, logger, verbose, storage_provider: GoogleCloudStorageProvider):
        self.logger = logger
        self.verbose = verbose
        self.storage_provider = storage_provider
        self.results = self._build_consent_list_structure()

    def add_result(self, result: ParsingResult):
        self.results[result.participant_id][result.type].append(result)

    def process_results(self):
        report_lines = []
        for validation_categories in self.results.values():
            if self.verbose:
                report_lines.append('')
            for result_list in validation_categories.values():
                for result in result_list:
                    report_lines.append(self._line_output_for_validation(result, verbose=self.verbose))

        self.logger.info('\n'.join(report_lines))

    def _line_output_for_validation(self, file: ParsingResult, verbose: bool):
        output_line = StringIO()
        if verbose:
            output_line.write(f'{str(file.id).ljust(8)} - ')
        output_line.write(f'P{file.participant_id} - {str(file.type).ljust(10)} ')

        if not file.file_exists:
            output_line.write('missing file')
        else:
            errors_with_file = []
            if not file.is_signature_valid:
                errors_with_file.append('invalid signature')
            if not file.is_signing_date_valid:
                errors_with_file.append(self._get_date_error_details(file, verbose))
            if file.other_errors is not None:
                errors_with_file.append(file.other_errors)

            output_line.write(', '.join(errors_with_file))
            if verbose:
                output_line.write(f'\n{self._get_link(file)}')

        return output_line.getvalue()

    @classmethod
    def _get_date_error_details(cls, file: ParsingResult, verbose: bool = False):
        extra_info = ''
        if verbose and file.signing_date and file.expected_sign_date:
            time_difference = file.signing_date - file.expected_sign_date
            extra_info = f', diff of {time_difference.days} days'
        return f'invalid signing date (expected {file.expected_sign_date} '\
               f'but file has {file.signing_date}{extra_info})'

    def _get_link(self, file: ParsingResult):
        bucket_name, *name_parts = file.file_path.split('/')
        blob = self.storage_provider.get_blob(
            bucket_name=bucket_name,
            blob_name='/'.join(name_parts)
        )
        return blob.generate_signed_url(datetime.utcnow() + timedelta(hours=2))


class _ValidationOutputHelper:
    """Class for containing generic and reusable code for output strategies"""

    @classmethod
    def get_new_validation_results(cls, existing_results: Collection[ParsingResult],
                                   results_to_filter: Collection[ParsingResult]):
        """
        Checks each validation result in results_to_filter
        and returns a list of results that are not in existing_results
        """
        return [file for file in results_to_filter if not cls._is_file_in_collection(file, existing_results)]

    @classmethod
    def _is_file_in_collection(cls, file: ParsingResult, file_collection: Collection[ParsingResult]):
        if file.file_exists:
            return any(
                [file.file_path == possible_matching_file.file_path for possible_matching_file in file_collection]
            ) or any(
                [file.type == possible_matching_file.type
                 and possible_matching_file.sync_status in
                 (ConsentSyncStatus.READY_FOR_SYNC, ConsentSyncStatus.SYNC_COMPLETE)
                 and file.participant_id == possible_matching_file.participant_id
                 for possible_matching_file in file_collection]
            )
        else:
            return any([
                file.type == possible_matching_file.type
                and file.participant_id == possible_matching_file.participant_id
                for possible_matching_file in file_collection
            ])


class ConsentValidationController:
    def __init__(self, consent_dao: ConsentDao, participant_summary_dao: ParticipantSummaryDao,
                 hpo_dao: HPODao, storage_provider: GoogleCloudStorageProvider):
        self.consent_dao = consent_dao
        self.participant_summary_dao = participant_summary_dao
        self.storage_provider = storage_provider

        self.va_hpo_id = hpo_dao.get_by_name('VA').hpoId

    @classmethod
    def build_controller(cls):
        return ConsentValidationController(
            consent_dao=ConsentDao(),
            participant_summary_dao=ParticipantSummaryDao(),
            hpo_dao=HPODao(),
            storage_provider=GoogleCloudStorageProvider()
        )

    def check_for_corrections(self, session):
        """Load all of the current consent issues and see if they have been resolved yet"""
        checks_needed = self.consent_dao.get_next_revalidate_batch(session)

        with UpdateResultStrategy(session=session, consent_dao=self.consent_dao) as storage_strategy:
            for participant_id, consent_type in checks_needed:
                participant_summary: ParticipantSummary = self.participant_summary_dao.get_with_session(
                    obj_id=participant_id,
                    session=session
                )
                validator = self._build_validator(participant_summary)

                if consent_type == ConsentType.PRIMARY:
                    storage_strategy.add_all(validator.get_primary_validation_results())
                elif consent_type == ConsentType.CABOR:
                    storage_strategy.add_all(validator.get_cabor_validation_results())
                elif consent_type == ConsentType.EHR:
                    storage_strategy.add_all(validator.get_ehr_validation_results())
                elif consent_type == ConsentType.GROR:
                    storage_strategy.add_all(validator.get_gror_validation_results())
                elif consent_type == ConsentType.PRIMARY_UPDATE:
                    storage_strategy.add_all(validator.get_primary_update_validation_results())

    def validate_consent_responses(self, summary: ParticipantSummary, output_strategy: ValidationOutputStrategy,
                                   consent_responses: Collection[ConsentResponse]):
        validator = self._build_validator(summary)
        validation_method_map = {
            ConsentType.PRIMARY: validator.get_primary_validation_results,
            ConsentType.CABOR: validator.get_cabor_validation_results,
            ConsentType.EHR: validator.get_ehr_validation_results,
            ConsentType.GROR: validator.get_gror_validation_results,
            ConsentType.PRIMARY_UPDATE: validator.get_primary_update_validation_results
        }

        for consent_response in consent_responses:
            get_validation_results_func = validation_method_map[consent_response.type]
            validation_results = self._process_validation_results(
                get_validation_results_func(expected_signing_date=consent_response.response.authored)
            )
            for result in validation_results:
                result.consent_response = consent_response
            output_strategy.add_all(validation_results)

    def validate_participant_consents(self, summary: ParticipantSummary, output_strategy: ValidationOutputStrategy,
                                      min_authored_date: date = None, max_authored_date: date = None,
                                      types_to_validate: Collection[ConsentType] = None):
        validator = self._build_validator(summary)

        if self._check_consent_type(ConsentType.PRIMARY, types_to_validate) and self._has_consent(
            consent_status=summary.consentForStudyEnrollment,
            authored=summary.consentForStudyEnrollmentFirstYesAuthored,
            min_authored=min_authored_date,
            max_authored=max_authored_date
        ):
            output_strategy.add_all(self._process_validation_results(validator.get_primary_validation_results()))
        if self._check_consent_type(ConsentType.CABOR, types_to_validate) and self._has_consent(
            consent_status=summary.consentForCABoR,
            authored=summary.consentForCABoRAuthored,
            min_authored=min_authored_date,
            max_authored=max_authored_date
        ):
            output_strategy.add_all(self._process_validation_results(validator.get_cabor_validation_results()))
        if self._check_consent_type(ConsentType.EHR, types_to_validate) and self._has_consent(
            consent_status=summary.consentForElectronicHealthRecords,
            authored=summary.consentForElectronicHealthRecordsAuthored,
            min_authored=min_authored_date,
            max_authored=max_authored_date
        ):
            output_strategy.add_all(self._process_validation_results(validator.get_ehr_validation_results()))
        if self._check_consent_type(ConsentType.GROR, types_to_validate) and self._has_consent(
            consent_status=summary.consentForGenomicsROR,
            authored=summary.consentForGenomicsRORAuthored,
            min_authored=min_authored_date,
            max_authored=max_authored_date
        ):
            output_strategy.add_all(self._process_validation_results(validator.get_gror_validation_results()))
        if self._check_consent_type(ConsentType.PRIMARY_UPDATE, types_to_validate) and self._has_primary_update_consent(
            summary=summary,
            min_authored=min_authored_date,
            max_authored=max_authored_date
        ):
            output_strategy.add_all(self._process_validation_results(validator.get_primary_update_validation_results()))

    def validate_consent_uploads(self, session: Session, output_strategy: ValidationOutputStrategy,
                                 min_consent_date=None, max_consent_date=None):
        """
        Find all the expected consents (filtering by dates if provided) and check the files that have been uploaded
        """
        validation_start_time = datetime.utcnow().replace(microsecond=0)

        # Retrieve consent response objects that need to be validated
        participant_id_consent_map = self.consent_dao.get_consent_responses_to_validate(session=session)
        participant_summaries = self.participant_summary_dao.get_by_ids_with_session(
            session=session,
            obj_ids=participant_id_consent_map.keys()
        )
        for summary in participant_summaries:
            self.validate_consent_responses(
                summary=summary,
                output_strategy=output_strategy,
                consent_responses=participant_id_consent_map[summary.participantId]
            )
        session.commit()

        # Use the legacy query for the day that the updated check is released (and in case any are missed)
        summaries_needing_validated = self.consent_dao.get_participants_with_unvalidated_files(session)
        logging.info(f'{len(summaries_needing_validated)} participants still needed validation')
        for summary in summaries_needing_validated:
            self.validate_participant_consents(
                summary=summary,
                output_strategy=output_strategy,
                min_authored_date=min_consent_date,
                max_authored_date=max_consent_date
            )

        # Queue a task to check for new errors to report to PTSC
        dispatch_check_consent_errors_task(validation_start_time)

    def validate_all_for_participant(self, participant_id: int, output_strategy: ValidationOutputStrategy):
        summary: ParticipantSummary = self.participant_summary_dao.get(participant_id)
        validator = self._build_validator(summary)

        if self._has_consent(consent_status=summary.consentForStudyEnrollment):
            output_strategy.add_all(validator.get_primary_validation_results())
        if self._has_consent(consent_status=summary.consentForCABoR):
            output_strategy.add_all(validator.get_cabor_validation_results())
        if self._has_consent(consent_status=summary.consentForElectronicHealthRecords):
            output_strategy.add_all(validator.get_ehr_validation_results())
        if self._has_consent(consent_status=summary.consentForGenomicsROR):
            output_strategy.add_all(validator.get_gror_validation_results())
        if self._has_primary_update_consent(summary):
            output_strategy.add_all(validator.get_primary_update_validation_results())

    @classmethod
    def _check_consent_type(cls, consent_type: ConsentType, to_check_list: Collection[ConsentType]):
        if to_check_list is None:
            return True
        else:
            return consent_type in to_check_list

    @classmethod
    def _process_validation_results(cls, results: List[ParsingResult]):
        ready_file = cls._find_file_ready_for_sync(results)
        if ready_file:
            return [ready_file]
        else:
            return results

    @classmethod
    def _has_consent(cls, consent_status, authored=None, min_authored=None, max_authored=None):
        return (
            consent_status == QuestionnaireStatus.SUBMITTED
            and (min_authored is None or authored > min_authored)
            and (max_authored is None or authored < max_authored)
        )

    @classmethod
    def _has_primary_update_consent(cls, summary: ParticipantSummary, min_authored=None, max_authored=None):
        if (
            (min_authored is None or summary.consentForStudyEnrollmentAuthored > min_authored)
            and (max_authored is None or summary.consentForStudyEnrollmentAuthored < max_authored)
        ):
            return (
                summary.consentCohort == ParticipantCohort.COHORT_1 and
                summary.consentForStudyEnrollmentAuthored.date() !=
                summary.consentForStudyEnrollmentFirstYesAuthored.date()
            )
        else:
            return False

    def _build_validator(self, participant_summary: ParticipantSummary) -> 'ConsentValidator':
        consent_factory = files.ConsentFileAbstractFactory.get_file_factory(
            participant_id=participant_summary.participantId,
            participant_origin=participant_summary.participantOrigin,
            storage_provider=self.storage_provider
        )
        return ConsentValidator(
            consent_factory=consent_factory,
            participant_summary=participant_summary,
            va_hpo_id=self.va_hpo_id
        )

    @classmethod
    def _organize_results(cls, results: Collection[ParsingResult]):
        """
        Organize the validation results by participant id and then
        consent type to make it easier for checking for updates for them
        """

        def new_participant_results():
            return defaultdict(lambda: [])
        organized_results = defaultdict(new_participant_results)
        for result in results:
            organized_results[result.participant_id][result.type].append(result)
        return organized_results

    @classmethod
    def _find_file_ready_for_sync(cls, results: List[ParsingResult]):
        for result in results:
            if result.sync_status == ConsentSyncStatus.READY_FOR_SYNC:
                return result

        return None

    @classmethod
    def _find_matching_validation_result(cls, new_result: ParsingResult, previous_results: List[ParsingResult]):
        """Return the corresponding object from the list. They're matched up based on the file path."""
        for previous_result in previous_results:
            if new_result.file_path == previous_result.file_path:
                return previous_result

        return None


class ConsentValidator:
    def __init__(self, consent_factory: files.ConsentFileAbstractFactory,
                 participant_summary: ParticipantSummary,
                 va_hpo_id: int):
        self.factory = consent_factory
        self.participant_summary = participant_summary
        self.va_hpo_id = va_hpo_id

        self._central_time = pytz.timezone('America/Chicago')

    def get_primary_validation_results(self, expected_signing_date: datetime = None) -> List[ParsingResult]:
        if expected_signing_date is None:
            expected_signing_date = self.participant_summary.consentForStudyEnrollmentFirstYesAuthored

        return self._generate_validation_results(
            consent_files=self.factory.get_primary_consents(),
            consent_type=ConsentType.PRIMARY,
            additional_validation=self._validate_is_va_file,
            expected_sign_datetime=expected_signing_date
        )

    def get_ehr_validation_results(self, expected_signing_date: datetime = None) -> List[ParsingResult]:
        if expected_signing_date is None:
            expected_signing_date = self.participant_summary.consentForElectronicHealthRecordsAuthored

        return self._generate_validation_results(
            consent_files=self.factory.get_ehr_consents(),
            consent_type=ConsentType.EHR,
            additional_validation=self._validate_is_va_file,
            expected_sign_datetime=expected_signing_date
        )

    def get_cabor_validation_results(self, expected_signing_date: datetime = None) -> List[ParsingResult]:
        if expected_signing_date is None:
            expected_signing_date = self.participant_summary.consentForCABoRAuthored

        return self._generate_validation_results(
            consent_files=self.factory.get_cabor_consents(),
            consent_type=ConsentType.CABOR,
            expected_sign_datetime=expected_signing_date
        )

    def get_gror_validation_results(self, expected_signing_date: datetime = None) -> List[ParsingResult]:
        if expected_signing_date is None:
            expected_signing_date = self.participant_summary.consentForGenomicsRORAuthored

        def check_for_checkmark(consent: files.GrorConsentFile, result):
            if not consent.is_confirmation_selected():
                result.other_errors = ConsentOtherErrors.MISSING_CONSENT_CHECK_MARK
                result.sync_status = ConsentSyncStatus.NEEDS_CORRECTING

        return self._generate_validation_results(
            consent_files=self.factory.get_gror_consents(),
            consent_type=ConsentType.GROR,
            additional_validation=check_for_checkmark,
            expected_sign_datetime=expected_signing_date
        )

    def get_primary_update_validation_results(self, expected_signing_date: datetime = None) -> List[ParsingResult]:
        if expected_signing_date is None:
            expected_signing_date = self.participant_summary.consentForStudyEnrollmentAuthored

        def extra_primary_update_checks(consent: files.PrimaryConsentUpdateFile, result):
            errors_detected = []

            if not consent.is_agreement_selected():
                errors_detected.append(ConsentOtherErrors.MISSING_CONSENT_CHECK_MARK)

            va_version_error_str = self._check_for_va_version_mismatch(consent)
            if va_version_error_str:
                errors_detected.append(va_version_error_str)

            if errors_detected:
                result.other_errors = ', '.join(errors_detected)
                result.sync_status = ConsentSyncStatus.NEEDS_CORRECTING

        return self._generate_validation_results(
            consent_files=self.factory.get_primary_update_consents(
                self.participant_summary.consentForStudyEnrollmentAuthored
            ),
            consent_type=ConsentType.PRIMARY_UPDATE,
            additional_validation=extra_primary_update_checks,
            expected_sign_datetime=expected_signing_date
        )

    def _check_for_va_version_mismatch(self, consent):
        is_va_consent = consent.get_is_va_consent()
        if self.participant_summary.hpoId == self.va_hpo_id and not is_va_consent:
            return ConsentOtherErrors.NON_VETERAN_CONSENT_FOR_VETERAN
        elif self.participant_summary.hpoId != self.va_hpo_id and is_va_consent:
            return ConsentOtherErrors.VETERAN_CONSENT_FOR_NON_VETERAN

        return None

    def _validate_is_va_file(self, consent, result: ParsingResult):
        mismatch_error_str = self._check_for_va_version_mismatch(consent)
        if mismatch_error_str:
            result.other_errors = mismatch_error_str
            result.sync_status = ConsentSyncStatus.NEEDS_CORRECTING

    def _generate_validation_results(self, consent_files: List[files.ConsentFile], consent_type: ConsentType,
                                     expected_sign_datetime: datetime,
                                     additional_validation=None) -> List[ParsingResult]:
        results = []
        for consent in consent_files:
            result = self._build_validation_result(consent, consent_type, expected_sign_datetime)
            if additional_validation:
                additional_validation(consent, result)
            results.append(result)

        if not results:
            results.append(ParsingResult(
                participant_id=self.participant_summary.participantId,
                file_exists=False,
                type=consent_type,
                sync_status=ConsentSyncStatus.NEEDS_CORRECTING
            ))
        return results

    def _build_validation_result(self, consent: files.ConsentFile, consent_type: ConsentType,
                                 expected_sign_datetime: datetime):
        """
        Used to check generic data found on all consent types,
        additional result information should be validated for each type
        """
        result = ParsingResult(
            participant_id=self.participant_summary.participantId,
            file_exists=True,
            type=consent_type,
            file_upload_time=consent.upload_time,
            file_path=consent.file_path
        )
        self._store_signature(result=result, consent_file=consent)

        result.signing_date = consent.get_date_signed()
        result.expected_sign_date = self._get_date_from_datetime(expected_sign_datetime)
        result.is_signing_date_valid = self._is_signing_date_valid(
            signing_date=result.signing_date,
            expected_date=result.expected_sign_date
        )

        if result.is_signature_valid and result.is_signing_date_valid:
            result.sync_status = ConsentSyncStatus.READY_FOR_SYNC
        else:
            result.sync_status = ConsentSyncStatus.NEEDS_CORRECTING

        return result

    @classmethod
    def _store_signature(cls, result: ParsingResult, consent_file: files.ConsentFile):
        signature = consent_file.get_signature_on_file()
        result.is_signature_valid = bool(signature)
        if signature is True:  # True returned for when images are found
            result.is_signature_image = True
        elif signature is not None:
            result.signature_str = signature[:ParsingResult.signature_str.type.length]

    @classmethod
    def _is_signing_date_valid(cls, signing_date, expected_date: date):
        if not signing_date or not expected_date:
            return False
        else:
            days_off = (signing_date - expected_date).days
            return abs(days_off) < 10

    def _get_date_from_datetime(self, timestamp: datetime):
        return timestamp.replace(tzinfo=pytz.utc).astimezone(self._central_time).date()
