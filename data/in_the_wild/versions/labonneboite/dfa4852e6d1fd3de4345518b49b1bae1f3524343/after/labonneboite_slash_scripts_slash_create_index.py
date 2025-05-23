# coding: utf8
import argparse
import contextlib
import logging
import os

import multiprocessing as mp
from cProfile import Profile
from pyprof2calltree import convert
from elasticsearch import Elasticsearch
from elasticsearch import TransportError
from elasticsearch.helpers import bulk
from sqlalchemy import inspect

from labonneboite.common import encoding as encoding_util
from labonneboite.common.util import timeit
from labonneboite.common import geocoding
from labonneboite.common import departements as dpt
from labonneboite.common import mapping as mapping_util
from labonneboite.common import pdf as pdf_util
from labonneboite.common import scoring as scoring_util
from labonneboite.common import es as lbb_es
from labonneboite.common.search import fetch_companies
from labonneboite.common.database import db_session
from labonneboite.common.load_data import load_ogr_labels, load_ogr_rome_mapping
from labonneboite.common.models import Office
from labonneboite.common.models import OfficeAdminAdd, OfficeAdminExtraGeoLocation, OfficeAdminUpdate, OfficeAdminRemove
from labonneboite.conf import settings

logging.basicConfig(level=logging.INFO, format='%(message)s')
# use this instead if you wish to investigate from which logger exactly comes each line of log
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERBOSE_LOGGER_NAMES = ['elasticsearch', 'sqlalchemy.engine.base.Engine', 'main', 'elasticsearch.trace']


class Profiling(object):
    ACTIVATED = False


@contextlib.contextmanager
def switch_es_index():
    """
    Context manager that will ensure that some code will operate on a new ES
    index. This new index will then be associated to the reference alias and
    the old index(es) will be dropped.

    Usage:

        with switch_es_index():
            # Here, all code will run on the new index
            run_some_code()

        # Here, the old indexes no longer exist and the reference alias points
        # to the new index
    """
    es = Elasticsearch()

    # Find current index names (there may be one, zero or more)
    alias_name = settings.ES_INDEX
    old_index_names = es.indices.get_alias(settings.ES_INDEX).keys()

    # Activate new index
    new_index_name = lbb_es.get_new_index_name()
    settings.ES_INDEX = new_index_name

    # Create new index
    lbb_es.create_index(new_index_name)

    try:
        yield
    except:
        # Delete newly created index
        lbb_es.drop_index(new_index_name)
        raise
    finally:
        # Set back alias name
        settings.ES_INDEX = alias_name

    # Switch alias
    # TODO this should be done in one shot with a function in es.py module
    lbb_es.add_alias_to_index(new_index_name)
    for old_index_name in old_index_names:
        es.indices.delete_alias(index=old_index_name, name=alias_name)

    # Delete old index
    for old_index_name in old_index_names:
        lbb_es.drop_index(old_index_name)


def get_verbose_loggers():
    return [logging.getLogger(logger_name) for logger_name in VERBOSE_LOGGER_NAMES]

def disable_verbose_loggers():
    """
    We disable some loggers at specific points of this script in order to have a clean output
    (especially of the sanity_check_rome_codes part) and avoid it being polluted by useless
    unwanted logs detailing every MysQL and ES request.
    """
    for logger in get_verbose_loggers():
        # For some unknown reason, logger.setLevel(logging.ERROR) here does not work as expected as
        # 'INFO' level messages are still visible. Hence we brutally disable the logger instead.
        # FIXME try again to increase logger level instead of disabling it.
        logger.disabled = True

def enable_verbose_loggers():
    for logger in get_verbose_loggers():
        logger.disabled = False

OFFICE_TYPE = 'office'
OGR_TYPE = 'ogr'
LOCATION_TYPE = 'location'
ES_TIMEOUT = 300
ES_BULK_CHUNK_SIZE = 10000  # default value is 500


class Counter(object):
    """
    Counter class without the race-condition bug.
    Needed to be able to have a variable (counter) shared between all parallel jobs.
    Inspired from https://stackoverflow.com/questions/2080660/python-multiprocessing-and-a-shared-counter
    """
    def __init__(self):
        self.val = mp.Value('i', 0)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value


completed_jobs_counter = Counter()


class StatTracker:
    def __init__(self):
        self.office_count = 0
        self.indexed_office_count = 0
        self.office_score_for_rome_count = 0
    def increment_office_count(self):
        self.office_count += 1
    def increment_indexed_office_count(self):
        self.indexed_office_count += 1
    def increment_office_score_for_rome_count(self):
        self.office_score_for_rome_count += 1

st = StatTracker()


# Below was an attempt at fixing the following issue:
# ElasticsearchException[Unable to find a field mapper for field [scores_by_rome.A0000]]
# which happens when a rome is orphaned (no company has a score for this rome).
#
# This attempt was unsuccessful but may be retried at some point. The idea was to ensure
# that scores_by_rome.%s fields were present in at least one office for every rome even orphaned ones.
#
# This raises a new issue:
# java.lang.NumberFormatException: Invalid shift value in prefixCoded bytes (is encoded value really an INT?)
# which is tricky to investigate.
#
# For full information about this issue see common/search.py/get_companies_from_es_and_db.
#
# for rome in mapping_util.MANUAL_ROME_NAF_MAPPING:
#     mapping_office["properties"]["scores_by_rome.%s" % rome] = {
#         "type": "integer",
#         "index": "not_analyzed",
#     }
#     mapping_office["properties"]["boosted_romes.%s" % rome] = {
#         "type": "integer",
#         "index": "not_analyzed",
#     }



def bulk_actions(actions):
    es = Elasticsearch(timeout=ES_TIMEOUT)
    # unfortunately parallel_bulk is not available in the current elasticsearch version
    # http://elasticsearch-py.readthedocs.io/en/master/helpers.html
    bulk(es, actions, chunk_size=ES_BULK_CHUNK_SIZE)


@timeit
def create_job_codes():
    """
    Create the `ogr` type in ElasticSearch.
    """
    logger.info("create job codes...")
    # libelles des appelations pour les codes ROME
    ogr_labels = load_ogr_labels()
    # correspondance appellation vers rome
    ogr_rome_codes = load_ogr_rome_mapping()
    actions = []

    for ogr, description in ogr_labels.iteritems():
        if ogr in ogr_rome_codes:
            rome_code = ogr_rome_codes[ogr]
            rome_description = settings.ROME_DESCRIPTIONS[rome_code]
            doc = {
                'ogr_code': ogr,
                'ogr_description': description,
                'rome_code': rome_code,
                'rome_description': rome_description
            }
            action = {
                '_op_type': 'index',
                '_index': settings.ES_INDEX,
                '_type': OGR_TYPE,
                '_source': doc
            }
            actions.append(action)
    bulk_actions(actions)


@timeit
def create_locations():
    """
    Create the `location` type in ElasticSearch.
    """
    actions = []
    for city in geocoding.get_cities():
        doc = {
            'city_name': city['name'],
            'location': {'lat': city['coords']['lat'], 'lon': city['coords']['lon']},
            'population': city['population'],
            'slug': city['slug'],
            'zipcode': city['zipcode'],
        }
        action = {
            '_op_type': 'index',
            '_index': settings.ES_INDEX,
            '_type': LOCATION_TYPE,
            '_source': doc
        }
        actions.append(action)

    bulk_actions(actions)


def get_office_as_es_doc(office):
    """
    Return the office as a JSON document suitable for indexation in ElasticSearch.
    The `office` parameter can be an `Office` or an `OfficeAdminAdd` instance.
    """
    # The `headcount` field of an `OfficeAdminAdd` instance has a `code` attribute.
    if hasattr(office.headcount, 'code'):
        headcount = office.headcount.code
    else:
        headcount = office.headcount

    try:
        headcount = int(headcount)
    except ValueError:
        headcount = 0

    # Cleanup exotic characters.
    sanitized_name = encoding_util.sanitize_string(office.office_name)
    sanitized_email = encoding_util.sanitize_string(office.email)
    sanitized_website = encoding_util.sanitize_string(office.website)

    doc = {
        'naf': office.naf,
        'siret': office.siret,
        'score': office.score,
        'headcount': headcount,
        'name': sanitized_name,
        'email': sanitized_email,
        'tel': office.tel,
        'website': sanitized_website,
        'department': office.departement,
        'flag_alternance': int(office.flag_alternance),
        'flag_junior': int(office.flag_junior),
        'flag_senior': int(office.flag_senior),
        'flag_handicap': int(office.flag_handicap),
    }

    if office.y and office.x:
        # Use an array to allow multiple locations per document, see https://goo.gl/fdTaEM
        # Multiple locations may be added later via the admin UI.
        doc['locations'] = [
            {'lat': office.y, 'lon': office.x},
        ]

    scores_by_rome, boosted_romes = get_scores_by_rome_and_boosted_romes(office)
    if scores_by_rome:
        doc['scores_by_rome'] = scores_by_rome
        doc['boosted_romes'] = boosted_romes

    return doc


def get_scores_by_rome_and_boosted_romes(office, office_to_update=None):
    scores_by_rome = {}
    boosted_romes = {}  # elasticsearch does not understand sets, so we use a dict of 'key => True' instead

    # fetch all rome_codes mapped to the naf of this office
    # as we will compute a score adjusted for each of them
    office_nafs = [office.naf]
    # Handle NAFs added to a company
    if office_to_update:
        office_nafs += office_to_update.as_list(office_to_update.nafs_to_add)

    romes_to_boost = []
    romes_to_remove = []
    if office_to_update:
        romes_to_boost = office_to_update.as_list(office_to_update.romes_to_boost)
        romes_to_remove = office_to_update.as_list(office_to_update.romes_to_remove)

    for naf in office_nafs:
        try:
            rome_codes = mapping_util.get_romes_for_naf(naf)
        except KeyError:
            # unfortunately some NAF codes have no matching ROME at all
            continue

        # Add unrelated rome for indexing (with boost) and remove unwanted romes
        rome_codes = set(rome_codes).union(set(romes_to_boost)) - set(romes_to_remove)

        for rome_code in rome_codes:
            score = 0

            # Manage office boosting
            if office_to_update and office_to_update.boost:
                if not office_to_update.romes_to_boost:
                    # Boost the score for all ROME codes.
                    boosted_romes[rome_code] = True
                elif rome_code in romes_to_boost:
                    # Boost the score for some ROME codes only.
                    boosted_romes[rome_code] = True

            score = scoring_util.get_score_adjusted_to_rome_code_and_naf_code(
                score=office.score,
                rome_code=rome_code,
                naf_code=naf)

            if score >= scoring_util.SCORE_FOR_ROME_MINIMUM or rome_code in boosted_romes:
                if rome_code in scores_by_rome:
                    if score > scores_by_rome[rome_code]:
                        scores_by_rome[rome_code] = score
                else:
                    scores_by_rome[rome_code] = score
                    st.increment_office_score_for_rome_count()

    return scores_by_rome, boosted_romes





def create_offices(disable_parallel_computing=False):
    """
    Populate the `office` type in ElasticSearch.
    Run it as a parallel computation based on departements.
    """
    if Profiling.ACTIVATED:
        func = profile_create_offices_for_departement
    else:
        func = create_offices_for_departement

    if disable_parallel_computing:
        for departement in dpt.DEPARTEMENTS:
            func(departement)
        return

    # Use parallel computing on all available CPU cores.
    # Use even slightly more than avaible CPUs because in practise a job does not always
    # use 100% of a cpu.
    # maxtasksperchild default is infinite, which means memory is never freed up, and grows indefinitely :-/
    # maxtasksperchild=1 ensures memory is freed up after every departement computation.
    pool = mp.Pool(processes=int(1.25*mp.cpu_count()), maxtasksperchild=1)
    pool.map(func, dpt.DEPARTEMENTS_WITH_LARGEST_ONES_FIRST)
    pool.close()
    pool.join()


@timeit
def create_offices_for_departement(departement):
    """
    Populate the `office` type in ElasticSearch with offices having given departement.
    """
    actions = []

    logger.info("STARTED indexing offices for departement=%s ...", departement)

    for _, office in enumerate(db_session.query(Office).filter_by(departement=departement).all()):

        st.increment_office_count()

        es_doc = get_office_as_es_doc(office)

        office_is_reachable = 'scores_by_rome' in es_doc

        if office_is_reachable:
            st.increment_indexed_office_count()
            actions.append({
                '_op_type': 'index',
                '_index': settings.ES_INDEX,
                '_type': OFFICE_TYPE,
                '_id': office.siret,
                '_source': es_doc,
            })

    bulk_actions(actions)

    completed_jobs_counter.increment()

    logger.info(
        "COMPLETED indexing offices for departement=%s (%s of %s jobs completed)",
        departement,
        completed_jobs_counter.value,
        len(dpt.DEPARTEMENTS),
    )

    display_performance_stats(departement)


def profile_create_offices_for_departement(departement):
    """
    Run create_offices_for_departement with profiling.
    """
    profiler = Profile()
    command = "create_offices_for_departement('%s')" % departement
    profiler.runctx(command, locals(), globals())
    relative_filename = 'profiling_results/create_index_dpt%s.kgrind' % departement
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_filename)
    convert(profiler.getstats(), filename)


@timeit
def add_offices():
    """
    Add offices (complete the data provided by the importer).
    """
    es = Elasticsearch(timeout=ES_TIMEOUT)

    for office_to_add in db_session.query(OfficeAdminAdd).all():

        office = Office.query.filter_by(siret=office_to_add.siret).first()

        # Only create a new office if it does not already exist.
        # This guarantees that the importer data will always have precedence.
        if not office:

            # The `headcount` field of an `OfficeAdminAdd` instance has a `code` attribute.
            if hasattr(office_to_add.headcount, 'code'):
                headcount = office_to_add.headcount.code
            else:
                headcount = office_to_add.headcount

            # Create the new office in DB.
            new_office = Office()
            # Use `inspect` because `Office` columns are named distinctly from attributes.
            for field_name in inspect(Office).columns.keys():
                try:
                    value = getattr(office_to_add, field_name)
                except AttributeError:
                    # Some fields are not shared between `Office` and `OfficeAdminAdd`.
                    continue
                if field_name == 'headcount':
                    value = headcount
                setattr(new_office, field_name, value)
            db_session.add(new_office)
            db_session.commit()

            # Create the new office in ES.
            doc = get_office_as_es_doc(office_to_add)
            es.create(index=settings.ES_INDEX, doc_type=OFFICE_TYPE, id=office_to_add.siret, body=doc)


@timeit
def remove_offices():
    """
    Remove offices (overload the data provided by the importer).
    """
    es = Elasticsearch(timeout=ES_TIMEOUT)

    # When returning multiple rows, the SQLAlchemy Query class can only give them out as tuples.
    # We need to unpack them explicitly.
    offices_to_remove = [siret for (siret,) in db_session.query(OfficeAdminRemove.siret).all()]

    for siret in offices_to_remove:
        # Apply changes in ElasticSearch.
        try:
            es.delete(index=settings.ES_INDEX, doc_type=OFFICE_TYPE, id=siret)
        except TransportError as e:
            if e.status_code != 404:
                raise
        # Apply changes in DB.
        office = Office.query.filter_by(siret=siret).first()
        if office:
            office.delete()
            # Delete the current PDF.
            pdf_util.delete_file(office)


@timeit
def update_offices():
    """
    Update offices (overload the data provided by the importer).
    """
    es = Elasticsearch(timeout=ES_TIMEOUT)

    for office_to_update in db_session.query(OfficeAdminUpdate).all():

        for siret in OfficeAdminUpdate.as_list(office_to_update.sirets):

            office = Office.query.filter_by(siret=siret).first()

            if office:
                # Apply changes in DB.
                office.email = u'' if office_to_update.remove_email else (office_to_update.new_email or office.email)
                office.email_alternance = u'' if office_to_update.remove_flag_alternance else (office_to_update.email_alternance or u'')
                office.tel = u'' if office_to_update.remove_phone else (office_to_update.new_phone or office.tel)
                office.website = u'' if office_to_update.remove_website else (office_to_update.new_website or office.website)
                office.flag_alternance = False if office_to_update.remove_flag_alternance else office.flag_alternance
                office.save()

                # Apply changes in ElasticSearch.
                body = {'doc':
                    {'email': office.email, 'phone': office.tel, 'website': office.website,
                    'flag_alternance': 1 if office.flag_alternance else 0}
                }

                scores_by_rome, boosted_romes = get_scores_by_rome_and_boosted_romes(office, office_to_update)
                if scores_by_rome:
                    body['doc']['scores_by_rome'] = scores_by_rome
                    body['doc']['boosted_romes'] = boosted_romes

                # The update API makes partial updates: existing `scalar` fields are overwritten,
                # but `objects` fields are merged together.
                # https://www.elastic.co/guide/en/elasticsearch/guide/1.x/partial-updates.html
                # However `scores_by_rome` and `boosted_romes` need to be overwritten because they
                # may change over time.
                # To do this, we perform 2 requests: the first one resets `scores_by_rome` and
                # `boosted_romes` and the second one populates them.
                delete_body = {'doc': {'scores_by_rome': None, 'boosted_romes': None}}

                # Unfortunately these cannot easily be bulked :-(
                # The reason is there is no way to tell bulk to ignore missing documents (404)
                # for a partial update. Tried it and failed it on Oct 2017 @vermeer.
                es.update(index=settings.ES_INDEX, doc_type=OFFICE_TYPE, id=siret, body=delete_body,
                        params={'ignore': 404})
                es.update(index=settings.ES_INDEX, doc_type=OFFICE_TYPE, id=siret, body=body,
                        params={'ignore': 404})

                # Delete the current PDF thus it will be regenerated at the next download attempt.
                pdf_util.delete_file(office)


@timeit
def update_offices_geolocations():
    """
    Remove or add extra geolocations to offices.
    New geolocations are entered into the system through the `OfficeAdminExtraGeoLocation` table.
    """
    es = Elasticsearch(timeout=ES_TIMEOUT)

    for extra_geolocation in db_session.query(OfficeAdminExtraGeoLocation).all():
        office = Office.query.filter_by(siret=extra_geolocation.siret).first()
        if office:
            locations = []
            if office.y and office.x:
                locations.append({'lat': office.y, 'lon': office.x})
            if not extra_geolocation.is_outdated():
                locations.extend(extra_geolocation.geolocations_as_lat_lon_properties())
                office.has_multi_geolocations = True
            else:
                office.has_multi_geolocations = False
            # Apply changes in DB.
            office.save()
            # Apply changes in ElasticSearch.
            body = {'doc': {'locations': locations}}
            es.update(index=settings.ES_INDEX, doc_type=OFFICE_TYPE, id=office.siret, body=body, params={'ignore': 404})


@timeit
def sanity_check_rome_codes():
    ogr_rome_mapping = load_ogr_rome_mapping()
    rome_labels = settings.ROME_DESCRIPTIONS
    rome_naf_mapping = mapping_util.MANUAL_ROME_NAF_MAPPING

    romes_from_ogr_rome_mapping = set(ogr_rome_mapping.values())
    romes_from_rome_labels = set(rome_labels.keys())
    romes_from_rome_naf_mapping = set(rome_naf_mapping.keys())

    subset1 = romes_from_ogr_rome_mapping - romes_from_rome_labels
    subset2 = romes_from_rome_labels - romes_from_ogr_rome_mapping
    subset3 = romes_from_rome_naf_mapping - romes_from_rome_labels
    subset4 = romes_from_rome_labels - romes_from_rome_naf_mapping

    msg = """
        -------------- SANITY CHECK ON ROME CODES --------------
        found %s distinct rome_codes in romes_from_ogr_rome_mapping
        found %s distinct rome_codes in romes_from_rome_labels
        found %s distinct rome_codes in romes_from_rome_naf_mapping

        found %s rome_codes present in romes_from_ogr_rome_mapping but not in romes_from_rome_labels: %s

        found %s rome_codes present in romes_from_rome_labels but not in romes_from_ogr_rome_mapping: %s

        found %s rome_codes present in romes_from_rome_naf_mapping but not in romes_from_rome_labels: %s

        found %s rome_codes present in romes_from_rome_labels but not in romes_from_rome_naf_mapping: %s
        """ % (
            len(romes_from_ogr_rome_mapping),
            len(romes_from_rome_labels),
            len(romes_from_rome_naf_mapping),
            len(subset1), subset1,
            len(subset2), subset2,
            len(subset3), subset3,
            len(subset4),
            # CSV style output for easier manipulation afterwards
            "".join(["\n%s|%s" % (r, rome_labels[r]) for r in subset4]),
        )
    logger.info(msg)

    city = geocoding.get_city_by_commune_id('75056')
    latitude = city['coords']['lat']
    longitude = city['coords']['lon']
    distance = 1000

    # CSV style output for easier manipulation afterwards
    logger.info("rome_id|rome_label|offices_in_france")
    for rome_id in romes_from_rome_naf_mapping:
        naf_code_list = mapping_util.map_romes_to_nafs([rome_id])
        disable_verbose_loggers()
        offices, _, _ = fetch_companies(
            naf_codes=naf_code_list,
            rome_code=rome_id,
            latitude=latitude,
            longitude=longitude,
            distance=distance,
            from_number=1,
            to_number=10,
        )
        enable_verbose_loggers()
        if len(offices) < 5:
            logger.info("%s|%s|%s", rome_id, rome_labels[rome_id], len(offices))


def display_performance_stats(departement):
    methods = [
               '_get_score_from_hirings',
               'get_hirings_from_score',
               'get_score_adjusted_to_rome_code_and_naf_code',
              ]
    for method in methods:
        logger.info("[DPT%s] %s : %s", departement, method, getattr(scoring_util, method).cache_info())

    logger.info("[DPT%s] indexed %s of %s offices and %s score_for_rome",
        departement,
        st.indexed_office_count,
        st.office_count,
        st.office_score_for_rome_count
    )


def update_data(create_full, create_partial, disable_parallel_computing):
    if create_partial:
        with switch_es_index():
            create_offices_for_departement('57')
        return

    if create_full:
        with switch_es_index():
            create_offices(disable_parallel_computing)
            create_job_codes()
            create_locations()

    # Upon requests received from employers we can add, remove or update offices.
    # This permits us to complete or overload the data provided by the importer.
    add_offices()
    remove_offices()
    update_offices()
    update_offices_geolocations()

    if create_full:
        sanity_check_rome_codes()


def update_data_profiling_wrapper(create_full, create_partial, disable_parallel_computing=False):
    if Profiling.ACTIVATED:
        logger.info("STARTED run with profiling")
        profiler = Profile()
        profiler.runctx(
            "update_data(create_full, create_partial, disable_parallel_computing)",
            locals(),
            globals()
        )
        relative_filename = 'profiling_results/create_index_run.kgrind'
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_filename)
        convert(profiler.getstats(), filename)
        logger.info("COMPLETED run with profiling: exported profiling result as %s", filename)
    else:
        logger.info("STARTED run without profiling")
        update_data(create_full, create_partial, disable_parallel_computing)
        logger.info("COMPLETED run without profiling")


def run():
    parser = argparse.ArgumentParser(
        description="Update elasticsearch data: offices, ogr_codes and locations.")
    parser.add_argument('-f', '--full', action='store_true',
        help="Create full index from scratch.")
    parser.add_argument('-a', '--partial', action='store_true',
        help=("Disable parallel computing and run only a single office indexing"
              " job (departement 57) instead. This is required in order"
              " to do a profiling from inside a job."))
    parser.add_argument('-p', '--profile', action='store_true',
        help="Enable code performance profiling for later visualization with Q/KCacheGrind.")
    args = parser.parse_args()

    if args.full and args.partial:
        raise ValueError('Cannot create both partial and full index at the same time')
    if args.profile:
        Profiling.ACTIVATED = True

    update_data_profiling_wrapper(args.full, args.partial)


if __name__ == '__main__':
    run()
