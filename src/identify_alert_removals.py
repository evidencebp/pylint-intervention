from os.path import join

import pandas as pd

from git_wrapper import GitWrapper
from process_content_dataframes import CHANGES_FILE
from utils import clone_repo, get_project_name

WILD_DIR = 'c:/in_the_wild'

def get_changed_files(alert_list: list
                      , change_types: list = ['removed']):
    df = pd.read_csv(CHANGES_FILE)
    df = df[df['msg'].isin(alert_list)]
    df = df[df['change'].isin(change_types)]

    return df

def clone_relevant_projects(alert_list: list
                            , target_dir:  str = WILD_DIR):

    df = get_changed_files(alert_list)

    for i in df['repo_name'].unique():
        print(i)
        clone_repo(i
                   , target_dir)

def find_change_commits(alert_list
                        , output: str = None):

    changed_files = get_changed_files(alert_list)

    changes = []
    for _, file in changed_files.iterrows():
        change_commits = find_file_change_commits(file['repo']
                                                    , file['path']
                                                    , alert_list)
        change_commits['repo_name'] = file['repo']
        change_commits['file'] = file['path']
        changes.append(change_commits)

    changes_df = pd.concat(changes)

    if output:
        changes_df.to_csv(output
                          , index=False)

    return changes_df

def find_file_change_commits(repo_name: str
                             , file_name: str
                             , alert_list) -> pd.DataFrame:

    gw = GitWrapper(join(WILD_DIR
                         , get_project_name(repo_name)))

    # Get files all commits from the first to the last

    # get first version and analyze it

    # Go over the rest of commits

        # Get commit version

        # Analyze alerts

        # Compare to previous version alerts

        # Add change

if __name__ == "__main__":
    alert_list = ['simplifiable-if-expression']
    #clone_relevant_projects(alert_list)
    find_change_commits(alert_list)

