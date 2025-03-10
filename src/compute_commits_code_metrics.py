from os.path import join

import pandas as pd

from compute_commits_diff import VERSIONS_DIR, WILD_DIR
from code_metrics import analyze_file, get_McCabe_complexity, get_repo_relevant_McCabe_stats
from utils import get_project_name, encode_path

def compute_commits_code_metrics(commits_df
                                 , path_format):
    all_metrics = []
    for _, i in commits_df.iterrows():
        repo_name = i['repo_name']
        project_name = get_project_name(repo_name)
        commit = i['commit']
        file_name = i['file_name']

        path = join(path_format.format(project_name=project_name
                                  , commit=commit)
                    , file_name)
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

    df = pd.concat(all_metrics)
    
    return df



def run_compute_commits_code_metrics():
    alert_change_commits_file = join(WILD_DIR
                                     , "alert_change_commits.csv")
    df = pd.read_csv(alert_change_commits_file)
    df = df[df['state'] == 'removed']

    # TODO - remove
    df = pd.DataFrame([('Flexget/Flexget', '1e7e0181d712b087dad29aa885ede37e8349ac6e', 'flexget/_version.py')]
                      , columns=['repo_name', 'commit', 'file_name'])
    
    before_path_format = VERSIONS_DIR + "/{project_name}/{commit}/before/"
    before_df = compute_commits_code_metrics(commits_df=df
                                 , path_format=before_path_format)
    before_df.to_csv(join(WILD_DIR
                          , 'before_commits_code_metrics.csv')
                     , index=False)


    after_path_format = VERSIONS_DIR + "/{project_name}/{commit}/after/"
    after_df = compute_commits_code_metrics(commits_df=df
                                 , path_format=after_path_format)
    after_df.to_csv(join(WILD_DIR
                          , 'after_commits_code_metrics.csv')
                     , index=False)

if __name__ == "__main__":
    run_compute_commits_code_metrics()


