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

def anecdotes(df):

    # Sum reduction reduce CCP in complexity alerts
    print("Reduction in McCabe sum")
    print(df[(df['McCabe_sum_diff']<-1)
                & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    print("Reduction in modified_McCabe_max_diff")
    print(df[(df['modified_McCabe_max_diff']<-1)
                & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # CCP increase after clean line too long reduction - no benefit seen
    print("clean changes")
    print(df[(df['is_clean']==True)
          & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # More benefit when CCP was high.
    # Check lift over regular change to see benefit over reduction to mean
    print("Change by CCP group")
    df['ccp_group'] = df['ccp_pm_before'].map(lambda x: 'low' if x < 0.09 else 'high' if x > 0.39 else 'med')
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['alert', 'ccp_group']
                                                            , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # Refactor is helpful with too-many-branches, too-many-nested-blocks
    print("Change by refactor")
    print(df[(df['is_refactor']==True)
          & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # Clean ratio
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['is_clean']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['alert', 'is_clean']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # Refactor ratio
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['is_refactor']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['alert', 'is_refactor']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # Only removal
    df['only_removal'] = df['removed_lines'].map(lambda x: x == 0)
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['only_removal']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['alert', 'only_removal']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))


def analyze_process_metrics():
    df = build_ds()

if __name__ == "__main__":
    analyze_process_metrics()
