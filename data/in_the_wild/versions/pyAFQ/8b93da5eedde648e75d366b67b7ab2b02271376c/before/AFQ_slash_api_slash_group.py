# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)  # noqa

import logging
import AFQ.data.s3bids as afs
from AFQ.api.participant import ParticipantAFQ
from AFQ.api.utils import wf_sections, add_method_descriptions
import AFQ.utils.streamlines as aus

import AFQ.viz.utils as vut
from dipy.utils.parallel import paramap

from dipy.io.stateful_tractogram import StatefulTractogram, Space
import dipy.tracking.streamlinespeed as dps
import dipy.tracking.streamline as dts

from AFQ.version import version as pyafq_version
import pandas as pd
import numpy as np
import os
import os.path as op
import json
import s3fs
from time import time
import nibabel as nib

from bids.layout import BIDSLayout
import bids.config as bids_config
try:
    bids_config.set_option('extension_initial_dot', True)
except ValueError:
    pass

try:
    import afqbrowser as afqb
    using_afqb = True
except (ImportError, ModuleNotFoundError):
    using_afqb = False


__all__ = ["GroupAFQ"]


# get rid of unnecessary columns in df
def clean_pandas_df(df):
    df = df.reset_index(drop=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


# this is parallelized below
def _getter_helper(wf_dict, attr_name):
    return wf_dict[attr_name]


@add_method_descriptions
class GroupAFQ(object):
    """
    """

    def __init__(self,
                 bids_path,
                 bids_filters={"suffix": "dwi"},
                 preproc_pipeline="all",
                 participant_labels=None,
                 output_dir=None,
                 parallel_params={"engine": "serial"},
                 bids_layout_kwargs={},
                 **kwargs):
        '''
        Initialize a GroupAFQ object from a BIDS dataset.

        Parameters
        ----------
        bids_path : str
            The path to preprocessed diffusion data organized in a BIDS
            dataset. This should contain a BIDS derivative dataset with
            preprocessed dwi/bvals/bvecs.
        bids_filters : dict
            Filter to pass to bids_layout.get when finding DWI files.
            Default: {"suffix": "dwi"}
        preproc_pipeline : str, optional.
            The name of the pipeline used to preprocess the DWI data.
            Default: "all".
        participant_labels : list or None, optional
            List of participant labels (subject IDs) to perform
            processing on. If None, all subjects are used.
            Default: None
        output_dir : str or None, optional
            Path to output directory. If None, outputs are put
            in a AFQ pipeline folder in the derivatives folder of
            the BIDS directory. pyAFQ will use existing derivatives
            from the output directory if they exist, instead of recalculating
            them (this means you need to clear the output folder if you want
            to recalculate a derivative).
            Default: None
        parallel_params : dict, optional
            Parameters to pass to paramap in AFQ.utils.parallel,
            to parallelize computations across subjects and sessions.
            Set "n_jobs" to -1 to automatically parallelize as
            the number of cpus. Here is an example for how to do
            multiprocessing with 4 cpus:
            {"n_jobs": 4, "engine": "joblib", "backend": "loky"}
            Default: {"engine": "serial"}
        bids_layout_kwargs: dict, optional
            Additional arguments to give to BIDSLayout from pybids.
            For large datasets, try:
            {"validate": False, "index_metadata": False}
            Default: {}
        kwargs : additional optional parameters
            You can set additional parameters for any step
            of the process. See :ref:`usage/kwargs` for more details.

        Examples
        --------
        api.GroupAFQ(my_path, csd_sh_order=4)
        api.GroupAFQ(
            my_path,
            reg_template_spec="mni_t2", reg_subject_spec="b0")
        '''
        if not isinstance(bids_path, str):
            raise TypeError("bids_path must be a string")
        if not op.exists(bids_path):
            raise ValueError("bids_path not found")
        if not op.exists(op.join(bids_path, "dataset_description.json")):
            raise ValueError("There must be a dataset_description.json"
                             + " in bids_path")
        if not isinstance(bids_filters, dict):
            raise TypeError("bids_filters must be a dict")
        # preproc_pipeline typechecking handled by pyBIDS
        if participant_labels is not None\
                and not isinstance(participant_labels, list):
            raise TypeError(
                "participant_labels must be either a list or None")
        if output_dir is not None\
                and not isinstance(output_dir, str):
            raise TypeError(
                "output_dir must be either a str or None")
        if not isinstance(parallel_params, dict):
            raise TypeError("parallel_params must be a dict")
        if not isinstance(bids_layout_kwargs, dict):
            raise TypeError("bids_layout_kwargs must be a dict")

        self.logger = logging.getLogger('AFQ.api')
        self.parallel_params = parallel_params
        self.wf_dict = {}

        # validate input and fail early
        if not op.exists(bids_path):
            raise ValueError(f'Unable to locate BIDS dataset in: {bids_path}')

        # This is where all the outputs will go:
        if output_dir is None:
            self.afq_path = op.join(bids_path, 'derivatives', 'afq')
            self.afqb_path = op.join(bids_path, 'derivatives', 'afq_browser')
        else:
            self.afq_path = output_dir
            self.afqb_path = op.join(output_dir, 'afq_browser')

        # Create it as needed:
        os.makedirs(self.afq_path, exist_ok=True)

        bids_layout = BIDSLayout(
            bids_path, derivatives=True, **bids_layout_kwargs)
        bids_description = bids_layout.description

        # check that any files exist in the derivatives folder,
        # not including the dataset_description.json files
        # the second check may be particularly useful in checking
        # that the derivatives folder is well-defined
        if len(bids_layout.get())\
                - len(bids_layout.get(extension="json")) < 1:
            raise ValueError(
                f"No non-json files recognized by pyBIDS in {bids_path}")
        if len(bids_layout.get(scope=preproc_pipeline))\
                - len(bids_layout.get(
                    scope=preproc_pipeline,
                    extension="json")) < 1:
            raise ValueError((
                f"No non-json files recognized by "
                f"pyBIDS in the pipeline: {preproc_pipeline}"))

        # Add required metadata file at top level (inheriting as needed):
        pipeline_description = {
            "Name": bids_description["Name"],
            "BIDSVersion": bids_description["BIDSVersion"],
            "PipelineDescription": {"Name": "pyAFQ",
                                    "Version": pyafq_version}}

        pl_desc_file = op.join(self.afq_path, 'dataset_description.json')

        with open(pl_desc_file, 'w') as outfile:
            json.dump(pipeline_description, outfile)

        self.subjects = bids_layout.get(return_type='id', target='subject')
        if not len(self.subjects):
            raise ValueError(
                "`bids_path` contains no subjects in derivatives folders."
                + " This could be caused by derivatives folders not following"
                + " the BIDS format.")

        if participant_labels is not None:
            filtered_subjects = []
            subjects_found_printed = False
            for subjectID in participant_labels:
                subjectID = str(subjectID)
                if subjectID not in self.subjects:
                    self.logger.warning((
                        f"Subject {subjectID} specified in "
                        f"`participant_labels` but not found "
                        f"in BIDS derivatives folders"))
                    if not subjects_found_printed:
                        subjects_found_printed = True
                        self.logger.warning((
                            f"Only these subjects found in BIDS "
                            f"derivatives folders: {self.subjects}"))
                else:
                    filtered_subjects.append(subjectID)
            self.subjects = filtered_subjects
            if not len(self.subjects):
                raise ValueError(
                    "No subjects specified in `participant_labels` "
                    + " found in BIDS derivatives folders."
                    + " See above warnings.")

        sessions = bids_layout.get(return_type='id', target='session')
        if len(sessions):
            self.sessions = sessions
        else:
            self.sessions = [None]

        # do not bother to parallelize if less than 2 subject-sessions
        if len(self.sessions) * len(self.subjects) < 2:
            self.parallel_params["engine"] = "serial"

        # do not parallelize segmentation if parallelizing across
        # subject-sessions
        if self.parallel_params["engine"] != "serial":
            if "segmentation_params" not in kwargs:
                kwargs["segmentation_params"] = {}
            if "parallel_segmentation" not in kwargs["segmentation_params"]:
                kwargs["segmentation_params"]["parallel_segmentation"] = {}
            kwargs["segmentation_params"]["parallel_segmentation"]["engine"] =\
                "serial"

        self.valid_sub_list = []
        self.valid_ses_list = []
        for subject in self.subjects:
            self.wf_dict[subject] = {}
            for session in self.sessions:
                this_kwargs = kwargs.copy()
                results_dir = op.join(self.afq_path, 'sub-' + subject)

                if session is not None:
                    results_dir = op.join(results_dir, 'ses-' + session)

                dwi_bids_filters = {
                    "subject": subject,
                    "session": session,
                    "return_type": "filename",
                    "scope": preproc_pipeline,
                    "extension": "nii.gz",
                    "suffix": "dwi",
                }
                dwi_bids_filters.update(bids_filters)
                dwi_files = bids_layout.get(**dwi_bids_filters)

                if (not len(dwi_files)):
                    self.logger.warning(
                        f"No dwi found for subject {subject} and session "
                        f"{session}. Skipping.")
                    continue

                os.makedirs(results_dir, exist_ok=True)
                dwi_data_file = dwi_files[0]

                # For bvals and bvecs, use ``get_bval()`` and ``get_bvec()`` to
                # walk up the file tree and inherit the closest bval and bvec
                # files. Maintain input ``bids_filters`` in case user wants to
                # specify acquisition labels, but pop suffix since it is
                # already specified inside ``get_bvec()`` and ``get_bval()``
                suffix = bids_filters.pop("suffix", None)
                bvec_file = bids_layout.get_bvec(
                    dwi_data_file,
                    **bids_filters)
                bval_file = bids_layout.get_bval(
                    dwi_data_file,
                    **bids_filters)
                if suffix is not None:
                    bids_filters["suffix"] = suffix

                self.valid_sub_list.append(subject)
                self.valid_ses_list.append(session)

                this_pAFQ = ParticipantAFQ(
                    dwi_data_file,
                    bval_file, bvec_file,
                    results_dir,
                    bids_info={
                        "bids_layout": bids_layout,
                        "subject": subject,
                        "session": session},
                    **this_kwargs)
                self.wf_dict[subject][str(session)] = this_pAFQ.wf_dict

    def __getattribute__(self, attr):
        # check if normal attr exists first
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            pass

        # find what name to use
        first_dict =\
            self.wf_dict[self.valid_sub_list[0]][str(self.valid_ses_list[0])]
        attr_name = None
        if attr in first_dict:
            attr_name = attr
            section = None
        else:
            for sub_attr in wf_sections:
                if attr in first_dict[sub_attr]:
                    attr_name = attr
                    section = sub_attr
                    break

        # attr not found, allow typical AttributeError
        if attr_name is None:
            return object.__getattribute__(self, attr)

        # iterate over subjects / sessions,
        # decide if they need to be calculated or not
        in_list = []
        to_calc_list = []
        results = {}
        for ii, subject in enumerate(self.valid_sub_list):
            if subject not in results:
                results[subject] = {}
            session = self.valid_ses_list[ii]
            wf_dict = self.wf_dict[subject][str(session)]
            if section is not None:
                wf_dict = wf_dict[section]
            if ((self.parallel_params.get("engine", False) != "serial")
                    and (hasattr(wf_dict, "efferents"))
                    and (attr_name not in wf_dict.efferents)):
                in_list.append((wf_dict))
                to_calc_list.append((subject, session))
            else:
                results[subject][session] =\
                    _getter_helper(wf_dict, attr_name)

        # if some need to be calculated, do those in parallel
        if len(to_calc_list) > 0:
            par_results = paramap(
                _getter_helper, in_list,
                func_args=[attr_name],
                **self.parallel_params)

            for i, subses in enumerate(to_calc_list):
                subject, session = subses
                results[subject][session] = par_results[i]

        # If only one session, collapse session dimension
        if len(self.sessions) == 1:
            for subject in self.valid_sub_list:
                results[subject] = results[subject][self.valid_ses_list[0]]

        return results

    def combine_profiles(self):
        tract_profiles_dict = self.profiles
        if len(self.sessions) > 1:
            tract_profiles_list = []
            for _, subject_dict in tract_profiles_dict.items():
                tract_profiles_list.extend(subject_dict.values())
        else:
            tract_profiles_list = list(tract_profiles_dict.values())
        _df = combine_list_of_profiles(tract_profiles_list)
        out_file = op.abspath(op.join(
            self.afq_path, "tract_profiles.csv"))
        os.makedirs(op.dirname(out_file), exist_ok=True)
        _df = clean_pandas_df(_df)
        _df.to_csv(out_file, index=False)
        return _df

    def get_streamlines_json(self):
        sls_json_fname = op.abspath(op.join(
            self.afq_path, "afqb_streamlines.json"))
        if not op.exists(sls_json_fname):
            subses_info = []

            def load_next_subject():
                subses_idx = len(subses_info)
                sub = self.valid_sub_list[subses_idx]
                ses = self.valid_ses_list[subses_idx]
                if len(self.sessions) > 1:
                    this_bundles_file = self.clean_bundles[sub][ses]
                    this_mapping = self.mapping[sub][ses]
                    this_img = nib.load(self.dwi[sub][ses])
                else:
                    this_bundles_file = self.clean_bundles[sub]
                    this_mapping = self.mapping[sub]
                    this_img = nib.load(self.dwi[sub])
                seg_sft = aus.SegmentedSFT.fromfile(
                    this_bundles_file,
                    this_img)
                seg_sft.sft.to_rasmm()
                subses_info.append((seg_sft, this_mapping))

            bundle_dict = self.bundle_dict[
                self.valid_sub_list[0]]
            if len(self.sessions) > 1:
                bundle_dict = bundle_dict[self.valid_ses_list[0]]

            sls_dict = {}
            load_next_subject()  # load first subject
            for b in bundle_dict.keys():
                if b != "whole_brain":
                    for i in range(len(self.valid_sub_list)):
                        seg_sft, mapping = subses_info[i]
                        idx = seg_sft.bundle_idxs[b]
                        # use the first subses that works
                        # otherwise try each successive subses
                        if len(idx) == 0:
                            # break if we run out of subses
                            if i + 1 >= len(self.valid_sub_list):
                                break
                            # load subses if not already loaded
                            if i + 1 >= len(subses_info):
                                load_next_subject()
                            continue
                        if len(idx) > 100:
                            idx = np.random.choice(
                                idx, size=100, replace=False)
                        these_sls = seg_sft.sft.streamlines[idx]
                        these_sls = dps.set_number_of_points(these_sls, 100)
                        tg = StatefulTractogram(
                            these_sls,
                            seg_sft.sft,
                            Space.RASMM)
                        delta = dts.values_from_volume(
                            mapping.forward,
                            tg.streamlines, np.eye(4))
                        moved_sl = dts.Streamlines(
                            [d + s for d, s in zip(delta, tg.streamlines)])
                        moved_sl = np.asarray(moved_sl)
                        median_sl = np.median(moved_sl, axis=0)
                        sls_dict[b] = {"coreFiber": median_sl.tolist()}
                        for ii, sl_idx in enumerate(idx):
                            sls_dict[b][str(sl_idx)] = moved_sl[ii].tolist()
                        break

            with open(sls_json_fname, 'w') as fp:
                json.dump(sls_dict, fp)
        return sls_json_fname

    def export_all(self, viz=True, afqbrowser=True, xforms=True,
                   indiv=True):
        """ Exports all the possible outputs

        Parameters
        ----------
        viz : bool
            Whether to output visualizations. This includes tract profile
            plots, a figure containing all bundles, and, if using the AFQ
            segmentation algorithm, individual bundle figures.
            Default: True
        afqbrowser : bool
            Whether to output an AFQ-Browser from this AFQ instance.
            Default: True
        xforms : bool
            Whether to output the reg_template image in subject space and,
            depending on if it is possible based on the mapping used, to
            output the b0 in template space.
            Default: True
        indiv : bool
            Whether to output individual bundles in their own files, in
            addition to the one file containing all bundles. If using
            the AFQ segmentation algorithm, individual ROIs are also
            output.
            Default: True
        """
        start_time = time()
        seg_params = self.segmentation_params[
            self.valid_sub_list[0]]
        if len(self.sessions) > 1:
            seg_params = seg_params[self.valid_ses_list[0]]
        seg_algo = seg_params.get("seg_algo", "AFQ")

        if xforms:
            try:
                self.b0_warped
            except Exception as e:
                self.logger.warning((
                    "Failed to export warped b0. This could be because your "
                    "mapping type is only compatible with transformation "
                    f"from template to subject space. The error is: {e}"))
            self.template_xform
        if indiv:
            self.indiv_bundles
            if seg_algo == "AFQ":
                self.rois
        self.sl_counts
        self.profiles
        # We combine profiles even if there is only 1 subject / session,
        # as the combined profiles format may still be useful
        # i.e., for AFQ Browser
        self.combine_profiles()
        if viz:
            try:
                self.tract_profile_plots
            except ImportError as e:
                plotly_err_message = vut.viz_import_msg_error("plot")
                if str(e) != plotly_err_message:
                    raise
                else:
                    self.logger.warning(plotly_err_message)
            self.all_bundles_figure
            if seg_algo == "AFQ":
                self.indiv_bundles_figures
        if afqbrowser:
            self.assemble_AFQ_browser()
        self.logger.info(
            "Time taken for export all: " + str(time() - start_time))

    def upload_to_s3(self, s3fs, remote_path):
        """ Upload entire AFQ derivatives folder to S3"""
        s3fs.put(self.afq_path, remote_path, recursive=True)
        if op.exists(self.afqb_path):
            s3fs.put(self.afqb_path, remote_path, recursive=True)

    def assemble_AFQ_browser(self, output_path=None, metadata=None,
                             page_title="AFQ Browser", page_subtitle="",
                             page_title_link="", page_subtitle_link=""):
        """
        Assembles an instance of the AFQ-Browser from this AFQ instance.
        First, we generate the combined tract profile if it is not already
        generated. This includes running the full AFQ pipeline if it has not
        already run. The combined tract profile is one of the outputs of
        export_all.
        Second, we generate a streamlines.json file from the bundle
        recognized in the first subject's first session.
        Third, we call AFQ-Browser's assemble to assemble an AFQ-Browser
        instance in output_path.

        Parameters
        ----------
        output_path : str
            Path to location to create this instance of the browser in.
            Called "target" in AFQ Browser API. If None,
            bids_path/derivatives/afq_browser is used.
            Default: None
        metadata : str
            Path to subject metadata csv file. If None, an metadata file
            containing only subject ID is created. This file requires a
            "subjectID" column to work.
            Default: None
        page_title : str
            Page title. If None, prompt is sent to command line.
            Default: "AFQ Browser"
        page_subtitle : str
            Page subtitle. If None, prompt is sent to command line.
            Default: ""
        page_title_link : str
            Title hyperlink (including http(s)://).
            If None, prompt is sent to command line.
            Default: ""
        page_subtitle_link : str
            Subtitle hyperlink (including http(s)://).
            If None, prompt is sent to command line.
            Default: ""
        """
        if not using_afqb:
            self.logger.warning((
                "AFQ Browser is not installed, so AFQ Browswer instance "
                "cannot be assembled. AFQ Browser can be installed with: "
                "`pip install pyAFQ[afqbrowser]` or "
                "`pip install AFQ-Browser>=0.3`"))
            return

        if output_path is None:
            output_path = self.afqb_path
        os.makedirs(self.afqb_path, exist_ok=True)

        # generate combined profiles csv
        self.combine_profiles()

        # generate streamlines.json file
        sls_json_fname = self.get_streamlines_json()

        afqb.assemble(
            op.abspath(op.join(self.afq_path, "tract_profiles.csv")),
            target=output_path,
            metadata=metadata,
            streamlines=sls_json_fname,
            title=page_title,
            subtitle=page_subtitle,
            link=page_title_link,
            sublink=page_subtitle_link)


def download_and_combine_afq_profiles(bucket,
                                      study_s3_prefix="", deriv_name=None,
                                      out_file=None,
                                      upload=False, session=None,
                                      **kwargs):
    """
    Download and combine tract profiles from different subjects / sessions
    on an s3 bucket into one CSV.
    Parameters
    ----------
    bucket : str
        The S3 bucket that contains the study data.
    study_s3_prefix : str
        The S3 prefix common to all of the study objects on S3.
    out_file : filename, optional
        Filename for the combined output CSV.
    deriv_name : str, optional
        If deriv_name is not None, it should be a string that specifies
        which derivatives folder to download and combine profiles from.
    upload : bool or str, optional
        If True, upload the combined CSV to Amazon S3 at
        bucket/study_s3_prefix/derivatives/afq. If a string,
        assume string is an Amazon S3 URI and upload there.
        Defaut: False
    session : str, optional
        Session to get CSVs from. If None, all sessions are used.
        Default: None
    kwargs : optional
        Optional arguments to pass to S3BIDSStudy.
    Returns
    -------
    Ouput CSV's pandas dataframe.
    """
    if "subjects" not in kwargs:
        kwargs["subjects"] = "all"
    if "anon" not in kwargs:
        kwargs["anon"] = False
    if deriv_name is None:
        deriv_name = True

    with nib.tmpdirs.InTemporaryDirectory() as t_dir:
        remote_study = afs.S3BIDSStudy(
            "get_profiles",
            bucket,
            study_s3_prefix,
            **kwargs)
        remote_study.download(
            t_dir,
            include_modality_agnostic=False,
            include_derivs=deriv_name,
            include_derivs_dataset_description=True,
            suffix="profiles.csv")
        temp_study = BIDSLayout(t_dir, validate=False, derivatives=True)
        if session is None:
            profiles = temp_study.get(
                extension='csv',
                suffix='profiles',
                return_type='filename')
        else:
            profiles = temp_study.get(
                session=session,
                extension='csv',
                suffix='profiles',
                return_type='filename')

        df = combine_list_of_profiles(profiles)
        df.to_csv("tmp.csv", index=False)
        if upload is True:
            bids_prefix = "/".join([bucket, study_s3_prefix]).rstrip("/")
            fs = s3fs.S3FileSystem()
            fs.put(
                "tmp.csv",
                "/".join([
                    bids_prefix,
                    "derivatives",
                    "afq",
                    "combined_tract_profiles.csv"
                ]))
        elif isinstance(upload, str):
            fs = s3fs.S3FileSystem()
            fs.put("tmp.csv", upload.replace("s3://", ""))

    if out_file is not None:
        out_file = op.abspath(out_file)
        os.makedirs(op.dirname(out_file), exist_ok=True)
        df = clean_pandas_df(df)
        df.to_csv(out_file, index=False)

    return df


def combine_list_of_profiles(profile_fnames):
    """
    Combine tract profiles from different subjects / sessions
    into one CSV.

    Parameters
    ----------
    profile_fnames : list of str
        List of csv filenames.

    Returns
    -------
    Ouput CSV's pandas dataframe.
    """
    dfs = []
    for fname in profile_fnames:
        profiles = pd.read_csv(fname)
        profiles['subjectID'] = fname.split('sub-')[1].split('/')[0]
        if 'ses-' in fname:
            session_name = fname.split('ses-')[1].split('/')[0]
        else:
            session_name = 'unknown'
        profiles['sessionID'] = session_name
        dfs.append(profiles)

    return clean_pandas_df(pd.concat(dfs))
