from os.path import join

import pandas as pd

from process_content_dataframes import CHANGES_FILE, CONFIG_FILE, TYPES_FILE

from utils import (clone_repo, get_project_name, get_all_commits, copy_file_at_commit, delete_directory
            , pylint_analysis)

WILD_DIR = 'c:/in_the_wild'

TOO_LARGE_REPOS = ['chromium/chromium']


def get_changed_files(alert_list: list
                      , change_types: list = ['removed']):
    df = pd.read_csv(CHANGES_FILE)
    if alert_list:
        df = df[df['msg'].isin(alert_list)]
    df = df[df['change'].isin(change_types)]

    df = df[~df['repo_name'].isin(TOO_LARGE_REPOS)]

    computed_df = pd.read_csv("C:/src/pylint-intervention/data/in_the_wild/alert_change_commits.csv")
    computed_df = computed_df[['repo_name',	'file_name', 'cur_count']]
    df = pd.merge(df
                  , computed_df
                  , left_on=['repo_name',	'path']
                  , right_on=['repo_name',	'file_name']
                  , how='left')
    df = df[df['cur_count'].isna()]

    return df

def clone_relevant_projects(alert_list: list
                            , target_dir:  str = WILD_DIR):

    df = get_changed_files(alert_list)

    print(f"Cloning {len(df['repo_name'].unique())} repositories")
    for i in df['repo_name'].unique():
        print(i)
        clone_repo(i
                   , target_dir)

def find_change_commits(alert_list
                        , output: str = None):

    types_df = pd.read_csv(TYPES_FILE)

    changed_files = get_changed_files(alert_list)
    changed_files = changed_files[~changed_files['repo_name'].isin(TOO_LARGE_REPOS)]

    print(f"Processing {len(changed_files)} files")

    changes = []
    file_num = 0
    for _, file in changed_files.iterrows():
        try:
            file_num = file_num + 1
            print("repo", file['repo_name'], "file", file['path'], "number", file_num)
            change_commits = find_file_change_commits(file['repo_name']
                                                        , file['path']
                                                        , alert_list
                                                        , types_df)
            if change_commits is not None:
                change_commits['repo_name'] = file['repo_name']
                change_commits['file'] = file['path']
                changes.append(change_commits)

        except Exception as e:
            print("Error processing", file, e)

        if len(changes):
            changes_df = pd.concat(changes)

            changes_df = changes_df.drop_duplicates()
            if output:
                changes_df.to_csv(output
                                  , index=False)

    return changes_df

def find_file_change_commits(repo_name: str
                             , file_name: str
                             , alert_list
                             , types_df) -> pd.DataFrame:

    TMP_FILE = 'c:/tmp/tmp.py'

    # Get files all commits from the first to the last
    repo_dir = join(WILD_DIR
                    , get_project_name(repo_name))
    commits_df = get_all_commits(repo_dir=repo_dir
                    , target=file_name)
    commits = list(reversed(commits_df.commit.tolist()))

    if commits is None or len(commits) == 0:
        # Seems to be due to deleted files
        # https://stackoverflow.com/questions/7203515/how-to-find-a-deleted-file-in-the-project-commit-history
        print("Error, no commits identified in ", repo_name, file_name)
        return None

    # get first version and analyze it
    prev_commit = commits[0]
    copy_file_at_commit(repo_dir=repo_dir
                            , source_file=file_name
                            , target_path=TMP_FILE
                            , commit=prev_commit)
    prev_alerts = pylint_analysis(target=TMP_FILE
                             , config=CONFIG_FILE
                             , types=types_df)

    delete_directory(TMP_FILE)

    changes = []
    # Go over the rest of commits
    for cur_commit in commits[1:]:

        # Get commit version
        copy_file_at_commit(repo_dir=repo_dir
                            , source_file=file_name
                            , target_path=TMP_FILE
                            , commit=cur_commit)

        # Analyze alerts
        cur_alerts = pylint_analysis(target=TMP_FILE
                                      , config=CONFIG_FILE
                                      , types=types_df)

        delete_directory(TMP_FILE)

        # Compare to previous version alerts
        for alert in alert_list:
            prev_count = (0 if prev_alerts is None or len(prev_alerts[prev_alerts['msg']==alert])==0
                          else prev_alerts[prev_alerts['msg']==alert].alerts.sum())
            cur_count = (0 if cur_alerts is None or len(cur_alerts[cur_alerts['msg']==alert])==0
                         else cur_alerts[cur_alerts['msg']==alert].alerts.sum())

            state = None
            # added
            if prev_count == 0 and cur_count > 0:
                state = 'added'
            elif prev_count > 0 and cur_count == 0:
                state = 'removed'
            elif prev_count < cur_count:
                state = 'increase'
            elif prev_count > cur_count:
                state = 'decrease'
            elif prev_count == cur_count:
                state = 'no change'

            # Add change
            if state != 'no change':
                changes.append((repo_name, file_name, alert
                                , cur_commit,  state, prev_count, cur_count))

        prev_alerts = cur_alerts

    changes_df = pd.DataFrame(changes
                              , columns=['repo_name', 'file_name', 'alert'
                                            , 'commit', 'state', 'prev_count', 'cur_count'])

    return changes_df

if __name__ == "__main__":
    processed = ['simplifiable-if-expression', 'too-many-branches', 'superfluous-parens', 'too-many-statements'
    , 'too-many-return-statements', 'too-many-nested-blocks', 'Simplify-boolean-expression', 'comparison-of-constants'
        , 'simplifiable-condition', 'too-many-boolean-expressions', 'unnecessary-semicolon'
        , 'simplifiable-if-statement', 'using-constant-test', 'try-except-raise', 'broad-exception-caught'
        , 'wildcard-import', 'unnecessary-pass', 'pointless-statement', 'too-many-lines']
    alert_list = ['line-too-long']
    clone_relevant_projects(alert_list)
    find_change_commits(alert_list
                        , output='c:/tmp/alert_change_commits.csv')

