"""

Getting code metrics using Radon
https://radon.readthedocs.io/en/latest/index.html
"""
import datetime
from os import listdir

from os.path import join
import numpy as np
import pandas as pd

from configuration import BASE_DIR, DONE_DIRECTORY, PROJECTS_DIR, PR_COL, REPO_COL
from code_metrics import analyze_file
from utils import (get_author_first_commit_in_repo, get_project_name, get_file_prev_commit
                    , get_branch_name, create_branch, checkout_branch, delete_branch
                    , get_branch_names)

BEFORE_DIR = join(BASE_DIR
                    , "data/code_metrics/before/")
AFTER_DIR = join(BASE_DIR
                    , "data/code_metrics/after/")

EXCLUDED_REPOS = ['aajanki_yle-dl_interventions_October_06_2024.csv'  # For some reason computation takes too long
                  ]


def get_metrics_file(repo_name):
    return repo_name.replace("/", "_slash_") + ".csv"

def get_done_interventions(interventions_file):
    df = pd.read_csv(interventions_file)
    df = df[~df[PR_COL].isna()]
    df = df[df[PR_COL].str.contains('github')]

    return df
def get_repo_metrics(interventions_file
                             , current=True
                             , verbose=False):
    df = get_done_interventions(interventions_file)

    repo_name = df[REPO_COL].max() # Should be same value, max takes one
    repo_dir = join(PROJECTS_DIR
                    , get_project_name(repo_name))

    pre_intervention_commit = None
    if not current:
        first_intervention_commit = get_author_first_commit_in_repo(repo_dir=repo_dir)
        pre_intervention_commit = get_file_prev_commit(commit=first_intervention_commit
                                                       , repo_dir=repo_dir)
        # Get current branch
        intervention_branch = get_branch_name(repo_dir=repo_dir)
        pre_branch_name = 'tmp_branch'

        # Move to pre-intervention branch
        create_branch(repo_dir=repo_dir
                          , branch_name='tmp_branch'
                          , commit=pre_intervention_commit)
        checkout_branch(repo_dir=repo_dir
                          , branch_name=pre_branch_name)


    metrics_list = []
    for _, i in df.iterrows():
        if verbose:
            print(datetime.datetime.now(), "analyzing ", i['path'])

        metrics = analyze_file(join(repo_dir
                            , i.path))
        metrics['path'] = i.path
        #metrics['commit'] = pre_intervention_commit

        if np.isreal(metrics['LOC']): # Avoid failure to analyze
            metrics_list.append(metrics)
        else:
            print("Not a real number LOC in ", interventions_file, i.path)

    metrics_df = pd.concat(metrics_list)

    if current:
        metrics_df.to_csv(join(AFTER_DIR
                           , get_metrics_file(repo_name))
                      , index=False)
    else:
        metrics_df.to_csv(join(BEFORE_DIR
                           , get_metrics_file(repo_name))
                      , index=False)

        # Return to original branch
        checkout_branch(repo_dir=repo_dir
                          , branch_name=intervention_branch)
        # Delete temp branch
        delete_branch(repo_dir=repo_dir
                      , branch_name=pre_branch_name)


def get_all_repo_metrics(current=True
                         , verbose: bool = False):

    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)


    for i in intervention_files:
        print(datetime.datetime.now(), i)
        get_repo_metrics(join(DONE_DIRECTORY
                              , i)
                                , current=current
                                , verbose=verbose)

def compute_code_differences(stats_per_repo=False):
    KEY= 'path'

    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)
    #intervention_files = ['mralext20_alex-bot_interventions_October_05_2024.csv'] # TODO - remove

    all_metrics = []
    for i in intervention_files:
        print(datetime.datetime.now(), i)

        intervention_df = pd.read_csv(join(DONE_DIRECTORY
                                           , i))
        intervention_df = intervention_df[~intervention_df[PR_COL].isna()]
        intervention_df = intervention_df[intervention_df[PR_COL].str.contains('github')]

        repo_name = intervention_df[REPO_COL].max()
        try:
            before_df = pd.read_csv(join(BEFORE_DIR
                                               , get_metrics_file(repo_name)))
            after_df = pd.read_csv(join(AFTER_DIR
                                               , get_metrics_file(repo_name)))
            metrics = pd.merge(before_df
                               , after_df
                               , on=KEY
                               , suffixes=('_before', '_after'))
            aggs = {'path': 'count'
                , 'msg': 'max'}
            for c in set(before_df.columns) - set([KEY, 'commit']):
                #print(c)
                try:
                    metrics['tmp_before'] = metrics[c + '_before'].map(lambda x: None if
                                    not (str(x).isnumeric() or isinstance(x, (int, float))) else float(x))
                    metrics['tmp_after'] = metrics[c + '_after'].map(lambda x: None if
                                    not (str(x).isnumeric() or isinstance(x, (int, float))) else float(x))
                    metrics[c + '_diff'] = metrics['tmp_after'] - metrics['tmp_before']
                    metrics.drop(columns=['tmp_before', 'tmp_after']
                                 , inplace=True)
                    #metrics[c + '_diff'] = metrics.apply(
                    #    lambda x: None if ('ERROR' in str([c + '_before'])) else x[c + '_after'] - x[c + '_before']
                    #    , axis=1
                    #)
                except TypeError:
                    print("Type error in", c, i)
                    metrics[c + '_diff'] = None
                aggs[c + '_diff'] = 'mean'

            joint = pd.merge(intervention_df
                             , metrics
                             , on=KEY)
            joint = joint[joint['alerts'] ==1] # Avoid multiple interventions in stats
            joint['file'] = i
            if stats_per_repo:
                g = joint.groupby(['msg_id']
                                           , as_index=False).agg(aggs)
                g.to_csv(join(BASE_DIR
                    , 'interventions/interventions_code_metrics_stats_{repo}.csv'.format(
                        repo=repo_name.replace('/','_'))))

            all_metrics.append(joint)

        except FileNotFoundError:
            print("A file was not found", i)

    all_metrics_df = pd.concat(all_metrics)
    all_metrics_df.to_csv(join(BASE_DIR
                            , 'interventions/interventions_code_metrics.csv')
                       , index=False)

    all_metrics_df['valid'] = all_metrics_df['LOC_before'].map(lambda x: str(x).isnumeric())
    all_metrics_df = all_metrics_df[all_metrics_df['valid'] == True]
    g = all_metrics_df.groupby(['msg_id']
                            , as_index=False).agg(aggs)
    g.to_csv(join(BASE_DIR
                            , 'interventions/interventions_code_metrics_stats.csv'))



def list_branches(func=get_branch_name):
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    for i in intervention_files:
        df = get_done_interventions(join(DONE_DIRECTORY
                              , i))
        repo_name = df[REPO_COL].max()  # Should be same value, max takes one
        repo_dir = join(PROJECTS_DIR
                        , get_project_name(repo_name))
        print(i)
        print(func(repo_dir=repo_dir))


interventions_file = "C:/src/pylint-intervention/interventions/done/mralext20_alex-bot_interventions_October_05_2024.csv"
#get_repo_metrics(interventions_file
#                 , current=False)
#get_all_current_repo_metrics()
#print(analyze_file("C:/src/alex-bot/alexBot/cogs/voiceCommands.py"))

#print(get_author_first_commit_in_repo("c:/interventions/alex-bot"))
"""
print(get_file_prev_commit(commit="0a6d54251d775b5111117de430683e2b6e7c3cb3"
                           , repo_dir="c:/interventions/alex-bot"))
print(show_file_content(file_name="alexBot\cogs\\reminders.py"
                            , repo_dir="c:/interventions/alex-bot"
                            , commit=get_file_prev_commit(commit="0a6d54251d775b5111117de430683e2b6e7c3cb3"
                           , repo_dir="c:/interventions/alex-bot")))
print("Compute current metrics")
get_all_repo_metrics(current=True)
print("Compute original metrics")
get_all_repo_metrics(current=False)
compute_code_differences(stats_per_repo=True)
"""
# TODO - branches not deleted
# TODO - Check metrics are correct
list_branches(get_branch_names)