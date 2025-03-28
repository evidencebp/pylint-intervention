"""

Getting code metrics using Radon
https://radon.readthedocs.io/en/latest/index.html
"""
import datetime
from os import listdir

from os.path import join
import numpy as np
import pandas as pd

from configuration import (BASE_DIR, DONE_DIRECTORY, PROJECTS_DIR, PR_COL, REPO_COL, EXCLUDED_REPOS
                                , BEFORE_DIR, AFTER_DIR, METRICS_BEFORE_DIR, METRICS_AFTER_DIR)
from code_metrics import analyze_file, get_McCabe_complexity, get_repo_relevant_McCabe_stats
from compute_diffs import DIFF_SIZE_FILE
from utils import (get_author_first_commit_in_repo, get_project_name, get_file_prev_commit
                    , get_branch_name, create_branch, checkout_branch, delete_branch
                    , force_dir, copy_files, get_done_interventions, encode_path)

INTERVENTIONS_CODE_METRICS_STATS = join(BASE_DIR
                            , 'interventions/interventions_code_metrics_stats.csv')


def get_metrics_file(repo_name):
    return encode_path(repo_name) + ".csv"


def get_repo_metrics(interventions_file
                             , current=True
                             , verbose=False):
    df = get_done_interventions(interventions_file)

    repo_name = df[REPO_COL].astype(str).max() # Should be same value, max takes one
    if current:
        repo_dir = join(AFTER_DIR
                    , get_project_name(repo_name))
        metrics_dir = METRICS_AFTER_DIR
    else:
        repo_dir = join(BEFORE_DIR
                    , get_project_name(repo_name))
        metrics_dir = METRICS_BEFORE_DIR

    metrics_list = []
    for _, i in df.iterrows():
        if verbose:
            print(datetime.datetime.now(), "analyzing ", i['path'])

        file = join(repo_dir
                            , encode_path(i.path))
        metrics = analyze_file(file)
        metrics['path'] = i.path

        McCabe_df = get_McCabe_complexity(file)
        McCabe_path = METRICS_AFTER_DIR if current else METRICS_BEFORE_DIR
        McCabe_path = join(McCabe_path
                           , 'McCabe'
                           , get_project_name(repo_name))
        force_dir(McCabe_path)
        McCabe_file = join(McCabe_path
                           ,encode_path(i.path).replace('.py', '.csv'))
        McCabe_df.to_csv(McCabe_file
                         , index=False)
        if np.isreal(metrics['LOC']): # Avoid failure to analyze
            metrics_list.append(metrics)
        else:
            print("Not a real number LOC in ", interventions_file, i.path)

    metrics_df = pd.concat(metrics_list)

    metrics_df.to_csv(join(metrics_dir
                           , get_metrics_file(repo_name))
                  , index=False)




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

    diff_df = pd.read_csv(DIFF_SIZE_FILE)
    diff_df = diff_df[diff_df['size']>0]

    all_metrics = []
    for i in intervention_files:
        print(datetime.datetime.now(), i)

        interventions_file = join(DONE_DIRECTORY
                                           , i)
        intervention_df = pd.read_csv(interventions_file)
        intervention_df = intervention_df[~intervention_df[PR_COL].isna()]
        intervention_df = intervention_df[intervention_df[PR_COL].str.contains('github')]

        repo_name = intervention_df[REPO_COL].astype(str).max()
        try:
            before_df = pd.read_csv(join(METRICS_BEFORE_DIR
                                         , get_metrics_file(repo_name)))
            after_df = pd.read_csv(join(METRICS_AFTER_DIR
                                        , get_metrics_file(repo_name)))
            metrics = pd.merge(before_df
                               , after_df
                               , on=KEY
                               , suffixes=('_before', '_after'))
            aggs = {'path': 'count'
                , 'msg': 'max'
                , 'modified_McCabe_max_diff': 'mean'
                    }
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
            joint = pd.merge(joint
                             , diff_df[[KEY]]
                             , on=KEY)
            modified_McCabe = get_repo_relevant_McCabe_stats(interventions_file)
            joint = pd.merge(joint
                             , modified_McCabe
                             , on='path'
                             , how='left')
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
    all_metrics_df.sort_values(['repo_name', 'msg'], inplace=True)
    all_metrics_df.to_csv(join(BASE_DIR
                                  , 'interventions/interventions_code_metrics.csv')
                       , index=False)

    all_metrics_df['valid'] = all_metrics_df['LOC_before'].map(lambda x: str(x).isnumeric())
    all_metrics_df = all_metrics_df[all_metrics_df['valid'] == True]

    get_metrics_dist(all_metrics_df)

    g = all_metrics_df.groupby(['msg_id']
                            , as_index=False).agg(aggs).sort_values('msg')
    g.to_csv(INTERVENTIONS_CODE_METRICS_STATS)


def compute_metrics_diff(before_df: pd.DataFrame
                         , after_df: pd.DataFrame
                         , key
                         , exclude_columns=[]):
    metrics = pd.merge(before_df
                       , after_df
                       , on=key
                       , suffixes=('_before', '_after'))
    aggs = {'path': 'count'
        , 'msg': 'max'
            }
    for c in set(before_df.columns) - set(key + exclude_columns):
        # print(c)
        try:
            metrics['tmp_before'] = metrics[c + '_before'].map(lambda x: None if
            not (str(x).isnumeric() or isinstance(x, (int, float))) else float(x))
            metrics['tmp_after'] = metrics[c + '_after'].map(lambda x: None if
            not (str(x).isnumeric() or isinstance(x, (int, float))) else float(x))
            metrics[c + '_diff'] = metrics['tmp_after'] - metrics['tmp_before']
            metrics.drop(columns=['tmp_before', 'tmp_after']
                         , inplace=True)
            # metrics[c + '_diff'] = metrics.apply(
            #    lambda x: None if ('ERROR' in str([c + '_before'])) else x[c + '_after'] - x[c + '_before']
            #    , axis=1
            # )
        except TypeError:
            print("Type error in", c)
            metrics[c + '_diff'] = None
        aggs[c + '_diff'] = 'mean'


    return metrics

def get_metrics_dist(df):
    alert = "line-too-long"
    print(alert)
    for i in ['SLOC_diff', 'LLOC_diff', 'LOC_diff']:
        print(i)
        print(df[df['msg']==alert][i].value_counts(normalize=True).sort_index().cumsum())

    alert = "too-many-branches"
    print(alert)
    for i in ['McCabe_sum_diff', 'modified_McCabe_max_diff']:
        print(i)
        print(df[df['msg']==alert][i].value_counts(normalize=True).sort_index().cumsum())

    #  simplifiable-if-expression
    alert = "simplifiable-if-expression"
    print(alert)
    for i in ['McCabe_sum_diff', 'modified_McCabe_max_diff']:
        print(i)
        print(df[df['msg']==alert][i].value_counts(normalize=True).sort_index().cumsum())

    alert = 'too-many-statements'
    print(alert)
    for i in ['McCabe_sum_diff', 'modified_McCabe_max_diff']:
        print(i)
        print(df[df['msg']==alert][i].value_counts(normalize=True).sort_index().cumsum())

def list_branches(func=get_branch_name):
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    for i in intervention_files:
        df = get_done_interventions(join(DONE_DIRECTORY
                              , i))
        repo_name = df[REPO_COL].astype(str).max()  # Should be same value, max takes one
        repo_dir = join(PROJECTS_DIR
                        , get_project_name(repo_name))
        print(i)
        print(func(repo_dir=repo_dir))


def get_pre_intervention_commits():
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    pre_intervention_commits = []
    for i in intervention_files:
        df = get_done_interventions(join(DONE_DIRECTORY
                              , i))
        repo_name = df[REPO_COL].astype(str).max()  # Should be same value, max takes one
        repo_dir = join(PROJECTS_DIR
                        , get_project_name(repo_name))
        first_intervention_commit = get_author_first_commit_in_repo(repo_dir=repo_dir)
        pre_intervention_commit = get_file_prev_commit(commit=first_intervention_commit
                                                       , repo_dir=repo_dir)
        pre_intervention_commits.append((repo_name, pre_intervention_commit))

    pre_intervention_commits_df = pd.DataFrame(pre_intervention_commits
                                               , columns=['repo_name', 'pre_intervention_commit'])
    pre_intervention_commits_df.to_csv(join(BASE_DIR
                                            , 'data/before'
                                            , 'pre_intervention_commits.csv')
                                       , index=False)

if __name__ == "__main__":
    #interventions_file = "C:/src/pylint-intervention/interventions/done/mralext20_alex-bot_interventions_October_05_2024.csv"
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

    """

    print("Compute current metrics")
    get_all_repo_metrics(current=True)
    print("Compute original metrics")
    get_all_repo_metrics(current=False)



    compute_code_differences(stats_per_repo=True)
#    get_pre_intervention_commits()
    #list_branches(get_branch_names)
