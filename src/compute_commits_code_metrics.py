import os
from os.path import join

import pandas as pd

from compute_code_metrics import compute_metrics_diff
from compute_commits_diff import VERSIONS_DIR, WILD_DIR
from code_metrics import analyze_file, get_McCabe_complexity, compute_modified_McCabe_max_diff
from utils import get_project_name, encode_path, copy_files

alert_change_commits_file = join(WILD_DIR
                                 , "alert_change_commits.csv")

AFTER_METRICS_FILE = join(WILD_DIR
                          , 'after_commits_code_metrics.csv')
BEFORE_METRICS_FILE = join(WILD_DIR
                           , 'before_commits_code_metrics.csv')

MODIFIED_MCCABE_FILE = join(WILD_DIR
                            , 'commits_modified_McCabe_max_diff.csv')


def compute_commits_code_metrics(commits_df
                                 , path_format):
    all_metrics = []

    print(f"Processing {len(commits_df)} commits")
    commit_num = 0
    for _, i in commits_df.iterrows():
        try:
            repo_name = i['repo_name']
            project_name = get_project_name(repo_name)
            commit = i['commit']
            file_name = i['file_name']
            commit_num += 1
            print(f"{commit_num} {repo_name} {file_name} {commit}")

            path = join(path_format.format(project_name=project_name
                                      , commit=commit)
                        , encode_path(file_name))

            metrics = analyze_file(path)

            metrics['repo_name'] = repo_name
            metrics['commit'] = commit
            metrics['path'] = file_name

            all_metrics.append(metrics)

            # McCabe
            McCabe_df = get_McCabe_complexity(path)
            McCabe_path = join(path_format.format(project_name=project_name
                                      , commit=commit)
                        , 'metrics'
                        , encode_path(file_name).replace('.py', '.csv'))
            McCabe_df.to_csv(McCabe_path
                             , index=False)
        except Exception as e:
            print("***********************************")
            print(f"Error processing {commit_num} {repo_name} {file_name} {commit}")
            print(e)

    df = pd.concat(all_metrics)
    
    return df



def run_compute_commits_code_metrics():
    df = pd.read_csv(alert_change_commits_file)
    df = df[df['state'] == 'removed']

    #df = pd.DataFrame([('Flexget/Flexget', '1e7e0181d712b087dad29aa885ede37e8349ac6e', 'flexget/_version.py')]
    #                  , columns=['repo_name', 'commit', 'file_name'])
    
    before_path_format = VERSIONS_DIR + "/{project_name}/{commit}/before/"
    before_df = compute_commits_code_metrics(commits_df=df
                                 , path_format=before_path_format)
    before_df = before_df.drop_duplicates()
    before_df.to_csv(BEFORE_METRICS_FILE
                     , index=False)


    after_path_format = VERSIONS_DIR + "/{project_name}/{commit}/after/"
    after_df = compute_commits_code_metrics(commits_df=df
                                 , path_format=after_path_format)
    after_df = after_df.drop_duplicates()
    after_df.to_csv(AFTER_METRICS_FILE
                     , index=False)

def compute_commits_metrics_diff():

    keys = ['repo_name', 'path', 'commit']
    before_df = pd.read_csv(BEFORE_METRICS_FILE)
    after_df = pd.read_csv(AFTER_METRICS_FILE)

    metrics_diff = compute_metrics_diff(before_df
                        , after_df
                        , key=keys)
    metrics_diff['valid'] = metrics_diff['LOC_before'].map(lambda x: str(x).isnumeric())
    metrics_diff = metrics_diff[metrics_diff['valid'] == True]

    df = pd.read_csv(alert_change_commits_file)

    joint = pd.merge(df
                     , metrics_diff
                     , left_on=['repo_name', 'file_name', 'commit']
                     , right_on=['repo_name', 'path', 'commit'])

    MCCabe_df = pd.read_csv(MODIFIED_MCCABE_FILE)
    joint = pd.merge(joint
                     , MCCabe_df
                     , on=['repo_name', 'file_name', 'commit'])
    joint.to_csv(join(WILD_DIR
                  , 'commits_code_metrics.csv')
             , index=False)

    agg = {'file_name': 'count', 'modified_McCabe_max_diff': 'mean'}
    for k in metrics_diff.columns:
        if '_diff' in k:
            agg[k] = 'mean'
    #agg = {k: 'mean' for k in metrics_diff.columns if '_diff' in k}

    g = joint.groupby(['alert', 'state']
                      , as_index=False).agg(agg).sort_values(['alert', 'state'])
    g.to_csv(join(WILD_DIR
                  , 'commits_code_metrics_diff_stats.csv')
             , index=False)

def get_McCabe_path(repo_name
                        , commit
                        , file_name
                        , position='before'):
    project_name = get_project_name(repo_name)

    path = (VERSIONS_DIR + f"/{project_name}/{commit}/{position}/metrics/"
                    + encode_path(file_name).replace('.py', '.csv'))

    return path


def get_commit_modified_McCabe_max_diff(repo_name
                                        , commit
                                        , file_name):

    before_path = get_McCabe_path(repo_name
                        , commit
                        , file_name
                        , position='before')
    before_df = pd.read_csv(before_path)
    after_path = get_McCabe_path(repo_name
                        , commit
                        , file_name
                        , position='after')
    after_df = pd.read_csv(after_path)
    modified_McCabe_max_diff = compute_modified_McCabe_max_diff(after_df
                                     , before_df)

    return modified_McCabe_max_diff

def compute_commits_modified_McCabe_max_diff():

    df = pd.read_csv(alert_change_commits_file)

    print(f"About to process {len(df)} records")
    commit_num = 0
    rows = []
    for _, i in df.iterrows():
        try:
            repo_name = i['repo_name']
            commit = i['commit']
            file_name = i['file_name']
            commit_num += 1
            print(f"{commit_num} {repo_name} {file_name} {commit}")
            modified_McCabe_max_diff = get_commit_modified_McCabe_max_diff(repo_name
                                            , commit
                                            , file_name)
            rows.append((repo_name, commit, file_name, modified_McCabe_max_diff))
        except Exception as e:
            print("Error processing", repo_name, commit, file_name)
            print(e)

    df = pd.DataFrame(rows
                      , columns=['repo_name', 'commit', 'file_name', 'modified_McCabe_max_diff'])
    df = df.drop_duplicates()
    df.to_csv(MODIFIED_MCCABE_FILE
             , index=False)

if __name__ == "__main__":
    #run_compute_commits_code_metrics()
    #compute_commits_modified_McCabe_max_diff()
    compute_commits_metrics_diff()


