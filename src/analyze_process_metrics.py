from os.path import join

import pandas
import pandas as pd

from compute_commits_diff import WILD_DIR
from compute_commit_profile import ENHANCED_FILE, extraction_candidates
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
    print(df[(df['McCabe_sum_diff']<0)
                & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    print("Reduction in modified_McCabe_max_diff - all alerts")
    print(df[(df['modified_McCabe_max_diff']<0)
             & (df['added_lines'] > 0)
             & (df['mostly_delete']==False)
                & (df['massive_change']==False)
                & (df.state.isin(['removed', 'decrease']))].agg({'commit': 'count', 'ccp_diff': 'mean'}))

    print("Reduction in modified_McCabe_max_diff")
    print(df[(df['modified_McCabe_max_diff']<0)
             & (df['added_lines'] > 0)
             & (df['mostly_delete']==False)
                & (df['massive_change']==False)
                & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))
    print("Reduction in modified_McCabe_max_diff by val and alert")
    for alert in extraction_candidates:
        print(alert)
        for diff in [0, -5, -10]:
            print(diff)
            print(df[(df['modified_McCabe_max_diff']<diff)
             & (df['added_lines'] > 0)
             & (df['mostly_delete']==False)
                & (df['massive_change']==False)
                & (df['alert']==alert)
                & (df.state.isin(['removed', 'decrease']))]
                    .groupby(['alert'])
                    .agg({'commit': 'count', 'ccp_diff': 'mean'}))


    print("added functions")
    print(df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['added_functions'] > 0)
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))]
            .groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    print("added functions")
    print(df[(df.state.isin(['removed'  # , 'decrease'
                             ]))
             & (df['added_functions'] > 0)
             & (df['alert'].isin(['too-many-branches'
                                     , 'too-many-nested-blocks'
                                     , 'too-many-return-statements'
                                     , 'too-many-statements']))]
          .groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    print("suitable added functions")
    print(df[(df.state.isin(['removed'  # , 'decrease'
                             ]))
             #& (df['modified_McCabe_max_diff']<diff)
             & (df['added_lines'] > 0)
             & (df['mostly_delete']==False)
                & (df['massive_change']==False)
             & (df['added_functions'] > 0)
             & (df['alert'].isin(['too-many-branches'
                                     , 'too-many-nested-blocks'
                                     , 'too-many-return-statements'
                                     , 'too-many-statements']))]
          .groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'
                                                , 'same_day_duration_avg_diff': 'mean'}))

    print("suitable alerts")
    print(df[(df.state.isin(['removed'  # , 'decrease'
                             ]))
             #& (df['modified_McCabe_max_diff']<diff)
             & (df['mostly_delete']==False)
                & (df['massive_change']==False)]
          .groupby(['alert']).agg({'commit': 'count'
                                                , 'ccp_diff': 'mean'
                                                , 'same_day_duration_avg_diff': 'mean'}))

    print("Reduction in modified_McCabe_max_diff, suitable diff")
    print(df[(df['modified_McCabe_max_diff']<0)
                & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))


    # CCP increases after clean line too long reduction - no benefit seen
    print("clean changes")
    print(df[(df['is_clean']==True)
          & (df.state.isin(['removed', 'decrease']))].groupby(['alert']).agg({'commit': 'count', 'ccp_diff': 'mean'}))

    # More benefit when CCP was high.
    # Check lift over regular change to see benefit over reduction to mean
    print("Change by CCP group")
    df['ccp_group'] = df['ccp_pm_before'].map(lambda x: 'low' if x < 0.09 else 'high' if x > 0.39 else 'med')
    print(df[(df.state.isin(['removed', 'decrease']))
             & (df['mostly_delete'] == False)
             & (df['massive_change'] == False)
             ].groupby(['alert', 'ccp_group']
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
    df['only_removal'] = df['added_lines'].map(lambda x: x == 0)
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['only_removal']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))
    print(df[df.state.isin(['removed', 'decrease'])].groupby(['alert', 'only_removal']
                                                , as_index=False).agg({'commit': 'count', 'ccp_diff': 'mean'}))


def experiment_candidates(df: pd.DataFrame):

    experiment_alerts = ['line-too-long'
                            , 'superfluous-parens'
                            , 'simplifiable-if-statement'
                            , 'simplifiable-if-expression'
                            , 'too-many-return-statements'
                            , 'too-many-branches'
                            , 'too-many-boolean-expressions'
                            ]

    df = df[df['state_x']=='removed']
    df = df[df['alert'].isin(experiment_alerts)]
    df = df[['alert', 'commit', 'repo_name', 'file_name_x', 'is_clean', 'is_refactor', 'added_functions']]
    df['is_refactor_label'] = ''
    df['is_clean_label'] = ''

    df = df.sample(frac=1.0)
    df.sort_values('alert'
                   , inplace=True)
    df.drop_duplicates(inplace=True)

    df.to_csv(join(WILD_DIR
                   , 'experiment_candidates.csv')
              , index=False)

    print(df.alert.value_counts())

def added_functions_hits(df: pandas.DataFrame):
    # added_functions

    print("added_functions hits")
    scope_df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))].copy()
    scope = len(scope_df)

    df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['added_functions'] > 0)
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))]
    print("hit_rate", len(df), "out of ", scope, len(df)/scope)

    write_labels(df
        , output_file=join(WILD_DIR
                       , 'added_functions_hits.csv')
        , columns_to_add=['is_refactor_label', 'is_clean_label', 'added_functions_label'])

    print(df.alert.value_counts())


def modified_McCabe_max_diff_hits(df: pandas.DataFrame):

    print("modified_McCabe_max_diff hits")
    scope_df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))].copy()
    scope = len(scope_df)

    df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['modified_McCabe_max_diff'] < 0)
            & (df['added_lines'] > 0)
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))]

    print("hit_rate", len(df), "out of ", scope, len(df)/scope)

    write_labels(df
        , output_file=join(WILD_DIR
                       , 'reduced_McCabe_max_hits.csv')
        , columns_to_add=['is_refactor_label', 'is_clean_label', 'reduced_McCabe_max_label'])

    print(df.alert.value_counts())


def suitable_modified_McCabe_max_diff_hits(df: pandas.DataFrame):

    print("modified_McCabe_max_diff hits")
    scope_df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))].copy()
    scope = len(scope_df)


    df = df[(df.state.isin(['removed'#, 'decrease'
                             ]))
            & (df['modified_McCabe_max_diff'] < 0)
            & (df['added_lines'] > 0)
            & (df['mostly_delete'] == False)
            & (df['massive_change'] == False)
            & (df['alert'].isin(['too-many-branches'
                                    , 'too-many-nested-blocks'
                                    , 'too-many-return-statements'
                                    , 'too-many-statements']))]

    print("hit_rate", len(df), "out of ", scope, len(df)/scope)

    write_labels(df
        , output_file=join(WILD_DIR
                       , 'suitable_reduced_McCabe_max_hits.csv')
        , columns_to_add=['is_refactor_label'
                            , 'is_clean_label'
                            , 'reduced_McCabe_max_label'
                            , 'mostly_delete'
                            , 'massive_change'])

    print(df.alert.value_counts())

def write_labels(df: pandas.DataFrame
                 , output_file
                 , columns_to_add: list = ['is_refactor_label', 'is_clean_label']):

    df = df[['alert', 'commit', 'repo_name', 'file_name_x', 'is_clean', 'is_refactor', 'added_functions']]

    for i in columns_to_add:
        df[i] = ''

    df = df.sample(frac=1.0)
    df.sort_values(['alert', 'repo_name']
                   , inplace=True)
    df.drop_duplicates(inplace=True)

    df.to_csv(output_file
              , index=False)

    print(df.alert.value_counts())

def ccp_by_alert():
    df = build_ds()

    print("Change by alert")
    print(df[(df.state.isin(['removed']))
             ].groupby(['alert']
             , as_index=False).agg({'commit': 'count'
                                    , 'ccp_diff': 'mean'
                                    ,  'same_day_duration_avg_diff': 'mean'}).sort_values(['commit']
                                                                                          , ascending =False))


def analyze_process_metrics():
    df = build_ds()
    anecdotes(df)
    experiment_candidates(df)
    df = build_ds()
    added_functions_hits(df)
    modified_McCabe_max_diff_hits(build_ds())
    suitable_modified_McCabe_max_diff_hits(build_ds())

if __name__ == "__main__":
    """
    analyze_process_metrics()
    df = build_ds()
    anecdotes(df)
    """
    ccp_by_alert()


