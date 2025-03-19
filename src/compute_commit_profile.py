"""
This code computes the profile of a commit - if it is clean and if it performs the needed refactor.
"""
import io
from os.path import join
import pandas as pd
import re

# commit textual analysis - bug fix
# only removals
# number of hunks
# refactor - added functions
# parenthesis removal
# if removal

from compute_commits_code_metrics import get_McCabe_path, alert_change_commits_file, get_diff_path
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

def get_diff_file(repo_name
                        , commit
                        , file_name):
    diff_path = get_diff_path(repo_name
                        , commit
                        , file_name)

    #with open(diff_path, 'r') as file:
    #    file_diff = file.read()
    file = io.open(diff_path, 'r', encoding='utf-16-le')
    diff = file.read()

    return diff

def get_hunks_num(file_diff):

    SNIPPET_REGEX = '@@ -(?P<offset1>\d+)(,(?P<len1>\d+))?\s\+(?P<name2>\d+)(,(?P<len2>\d+))?\s@@'

    snippets_matches = re.findall(SNIPPET_REGEX, file_diff)
    snippets = [(int(m[0]), int(m[2] or 0)) for m in snippets_matches]

    snippets = sorted(snippets, key=lambda x: x[0])

    return len(snippets)


def get_changed_lines(file_diff
                      , is_added):

    if is_added:
        lines = re.findall('\\n\+', file_diff)
        hunks = re.findall('\\n\+\+\+', file_diff)
    else:
        lines = re.findall('\\n\-', file_diff)
        hunks = re.findall('\\n\-\-\-', file_diff)

    return len(lines) - len(hunks)


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
            diff = get_diff_file(repo_name
                        , commit
                        , file_name)

            hunks_num = get_hunks_num(diff)

            added_lines = get_changed_lines(diff
                      , is_added=True)
            removed_lines = get_changed_lines(diff
                      , is_added=False)
            changed_lines = added_lines + removed_lines
            added_functions = get_added_functions(repo_name
                        , commit
                        , file_name)
            rows.append((repo_name, commit, file_name, added_functions, hunks_num
                         , added_lines, removed_lines, changed_lines))
        except Exception as e:
            print("Error processing", repo_name, commit, file_name)
            print(e)

    df = pd.DataFrame(rows
                      , columns=['repo_name', 'commit', 'file_name', 'added_functions', 'hunks_num'
                                 , 'added_lines', 'removed_lines', 'changed_lines'])
    df = df.drop_duplicates()
    df.to_csv(PROFILES_FILE
             , index=False)


if __name__ == "__main__":
    compute_commit_profiles()



