from os.path import join
import pandas as pd

from configuration import BASE_DIR
from utils import count_repo_recent_commits, pull_repo, get_project_name

REPOS_DIR = "c:/interventions/"
days_list = [7, 30, 90]


def get_commits_by_days(repo_dir: str
                               , days_list):

    result = {}
    for days in days_list:
        commits = count_repo_recent_commits(repo_dir=repo_dir
                                  , days=days)
        result[days] = commits

    return result

def get_project_recent_commits(repo_name: str
                                , pull_first: bool=False):


    if pull_first:
        pull_repo(repo_name=repo_name
                 , target_dir=REPOS_DIR)

    result = get_commits_by_days(repo_dir=join(REPOS_DIR
                                                      , get_project_name(repo_name))
                               , days_list=days_list)
    return result

def project_recent_commits(pull_first: bool=False
                           , output: str = None):

    CANDIDATES_FILE = join(BASE_DIR
                       , 'interventions/candidates_detailed_stats.csv')

    candidates_df = pd.read_csv(CANDIDATES_FILE)

    dfs = []
    cnt = 1
    for file in candidates_df.file_name.unique():


        repo_name = file[:file.find("_interventions")].replace('_', '/', 1)

        result = get_project_recent_commits(repo_name=repo_name
                                    , pull_first=pull_first)
        result["file_name"] = file
        result["repo_name"] = repo_name

        result_df = pd.DataFrame(result, index=[0])
        result_df = result_df[["file_name", "repo_name"]
                                + days_list]
        dfs.append(result_df)

        cnt = cnt + 1
        if cnt % 100 == 0:
            print("Processed {cnt} repos".format(cnt=cnt))

    all_df = pd.concat(dfs)

    if output:
        all_df.to_csv(output
                      , index=False)
    return all_df

def combine():
    #recent_df = project_recent_commits(pull_first=True
    #                        , output=join(BASE_DIR
    #                   , 'interventions/candidates_recent_commits.csv'))
    recent_df = pd.read_csv(join(BASE_DIR
                       , 'interventions/candidates_recent_commits.csv'))

    CANDIDATES_FILE = join(BASE_DIR
                       , 'interventions/candidates_detailed_stats.csv')
    candidates_df = pd.read_csv(CANDIDATES_FILE)

    joint = pd.merge(candidates_df, recent_df, on='file_name', how='left')

    joint.to_csv(join(BASE_DIR
                       , 'interventions/candidates_detailed_stats_with_recent.csv')
                 , index=False)

if __name__ == "__main__":
    combine()