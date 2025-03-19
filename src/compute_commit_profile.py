"""
This code computes the profile of a commit - if it is clean and if it performs the needed refactor.
"""
from os.path import join
import pandas as pd

# commit textual analysis - bug fix
# only removals
# number of hunks
# refactor - added functions
# parenthesis removal
# if removal

from compute_commits_code_metrics import get_McCabe_path, alert_change_commits_file
from compute_commits_diff import WILD_DIR


PROFILES_FILE = join(WILD_DIR
                            , 'commit_profiles.csv')

def get_added_functions(repo_name
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

    joint = pd.merge(after_df[['name', 'complexity']]
                        , before_df[['name', 'complexity']]
                        , on=['name']
                        , how='left'
                        , suffixes=('_after', '_before'))
    added_functions = len(joint[joint['complexity_before'].isna()])

    return added_functions

def get_hunks_num(repo_name
                        , commit
                        , file_name):
    pass

def compute_commit_profiles():
    df = pd.read_csv(alert_change_commits_file)
    df = df[['repo_name', 'commit', 'file_name']].drop_duplicates()

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
            added_functions = get_added_functions(repo_name
                        , commit
                        , file_name)
            rows.append((repo_name, commit, file_name, added_functions))
        except Exception as e:
            print("Error processing", repo_name, commit, file_name)
            print(e)

    df = pd.DataFrame(rows
                      , columns=['repo_name', 'commit', 'file_name', 'added_functions'])
    df = df.drop_duplicates()
    df.to_csv(PROFILES_FILE
             , index=False)


if __name__ == "__main__":
    compute_commit_profiles()



