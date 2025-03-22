from os.path import join

import pandas as pd

from compute_commits_diff import WILD_DIR
from compute_commit_profile import ENHANCED_FILE
from compute_commits_code_metrics import alert_change_commits_file

def build_process_metrics_ds(all_time: bool = False
                             , min_commits: int = 5):
    dir_path = join(WILD_DIR
                     , 'stats')

    file_format = "file_properties_{position}_anchor{period}.csv"

    before = file_format.format(position="before"
                                , period="" if all_time else "_3m")
    before_df = pd.read_csv(join(dir_path
                                 , before))
    after = file_format.format(position="after"
                                , period="" if all_time else "_3m")
    after_df = pd.read_csv(join(dir_path
                                 , after))

    if min_commits:
        before_df = before_df[before_df['commits']>= min_commits]
        after_df = after_df[after_df['commits']>= min_commits]

    joint_pm = pd.merge(before_df
                     , after_df
                     , on=['repo_name', 'file', 'commit']
                     , suffixes=('_pm_before', '_pm_after'))

    diff_metrics = ['ccp', 'refactor_mle', 'avg_coupling_code_size_cut', 'same_day_duration_avg', 'one_file_fix_rate']
    for i in diff_metrics:
        joint_pm[i + "_diff"] = joint_pm[i + '_pm_after'] - joint_pm[i + '_pm_before']

    return joint_pm

def build_ds():
    # all commits
    df = pd.read_csv(alert_change_commits_file)

    # process metrics
    process_df = build_process_metrics_ds(all_time=False
                             , min_commits=5)
    #process_df.rename(columns={'file': 'file_name'}
    #                  , inplace=True)
    df = pd.merge(df
                  , process_df
                  , how='left'
                  , on=['repo_name', 'file', 'commit'])
    # profile
    enhanced_df = pd.read_csv(ENHANCED_FILE)
    df = pd.merge(df
                  , enhanced_df
                  , how='left'
                  , on=['repo_name', 'file', 'commit', 'alert'])

    # code metrics
    code_metrics_df = pd.read_csv(join(WILD_DIR
                  , 'commits_code_metrics.csv'))
    df = pd.merge(df
                  , code_metrics_df
                  , how='left'
                  , on=['repo_name', 'file', 'commit', 'alert'])

    return df

def analyze_process_metrics():
    df = build_ds()

if __name__ == "__main__":
    analyze_process_metrics()
