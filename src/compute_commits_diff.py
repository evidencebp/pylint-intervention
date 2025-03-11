from os.path import join

import pandas as pd

from configuration import DATA_DIR
from utils import (get_project_name, force_dir, copy_file_at_commit, encode_path, get_file_prev_commit
        , run_powershell_cmd)

WILD_REPOS_DIR = 'c:/in_the_wild'

WILD_DIR = join(DATA_DIR
                , "in_the_wild")
VERSIONS_DIR = join(WILD_DIR
                , "versions")

def create_commit_version_directories(versions_dir
                                      , repo_name
                                      , commit):
    project_name = get_project_name(repo_name)
    repo_dir = join(versions_dir
                    , project_name)
    force_dir(repo_dir)

    commit_dir = join(repo_dir
                    , commit)

    force_dir(commit_dir)

    force_dir(join(commit_dir
                   , 'before'))
    force_dir(join(commit_dir
                   , 'before'
                   , 'metrics'))

    force_dir(join(commit_dir
                   , 'after'))
    force_dir(join(commit_dir
                   , 'after'
                   , 'metrics'))

    force_dir(join(commit_dir
                   , 'diffs'))


def compute_commits_diff(commits_df):

    for _, i in commits_df.iterrows():

        repo_name = i['repo_name']
        cur_commit = i['commit']
        file_name = i['file_name']

        # Verify needed directories exist
        create_commit_version_directories(VERSIONS_DIR
                                          , i['repo_name']
                                          , i['commit'])

        project_name = get_project_name(repo_name)
        repo_code_dir = join(WILD_REPOS_DIR
                    , project_name)


        # Copy commit version
        after_version = join(VERSIONS_DIR
                                               , project_name
                                               , cur_commit
                                               , 'after'
                                               , encode_path(file_name))
        copy_file_at_commit(repo_dir=repo_code_dir
                            , source_file=file_name
                            , target_path=after_version
                            , commit=cur_commit)

        # Copy previous commit version
        pre_intervention_commit = get_file_prev_commit(commit=cur_commit
                                                       , repo_dir=repo_code_dir)
        before_version = join(VERSIONS_DIR
                                               , project_name
                                               , cur_commit
                                               , 'before'
                                               , encode_path(file_name))
        copy_file_at_commit(repo_dir=repo_code_dir
                            , source_file=file_name
                            , target_path=join(VERSIONS_DIR
                                               , project_name
                                               , cur_commit
                                               , 'before'
                                               , encode_path(file_name))
                            , commit=pre_intervention_commit)


        diff_file = join(VERSIONS_DIR
                                               , project_name
                                               , cur_commit
                                               , 'diffs'
                                               , encode_path(file_name).replace('.py', '.txt'))
        cmd = f"cd {repo_code_dir}; git diff {after_version} {before_version} > {diff_file}"
        run_powershell_cmd(cmd)


def run_compute_commits_diff():
    alert_change_commits_file = join(WILD_DIR
                                        , "alert_change_commits.csv")
    df = pd.read_csv(alert_change_commits_file)
    df = df[df['state']=='removed']

    # TODO - remove
    df = pd.DataFrame([('Flexget/Flexget', '1e7e0181d712b087dad29aa885ede37e8349ac6e', 'flexget/_version.py')]
                      , columns=['repo_name', 'commit', 'file_name'])
    compute_commits_diff(df)

if __name__ == "__main__":
    run_compute_commits_diff()
