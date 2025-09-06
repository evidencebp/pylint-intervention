import os
import sys

ANALYSIS_PATH = r'c:\src\analysis_utils'
sys.path.append(ANALYSIS_PATH)

from analysis_utils.ml_utils import build_and_eval_models, save_performance, build_models
from analysis_utils.feature_pair_analysis import pair_features_vs_concept, features_stats_to_cm_df

from configuration import BASE_DIR
from compute_commit_profile import extraction_candidates
from analyze_process_metrics import build_ds

PERFORMANCE_DIR = os.path.join(BASE_DIR
                                , r'performance')
PERFORMANCE_PATH = os.path.join(PERFORMANCE_DIR
                                , 'ccp_reduction_cm.csv')
MODELS_PATH = os.path.join(BASE_DIR, r'models')

from os.path import join
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier

class_weight = {1: 1, 0: 1}

MIN_SAMPLES = 10
MAX_DEPTH = 3

classifiers = {'Tree_ms50_md3': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                                               , max_depth=MAX_DEPTH
                                                               , class_weight=class_weight)
    , 'Tree_default': DecisionTreeClassifier(class_weight=class_weight)
    , 'Tree_ms50': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                          , class_weight=class_weight)
    , 'Tree_md3': DecisionTreeClassifier(max_depth=MAX_DEPTH
                                         , class_weight=class_weight)
    , 'RandomForest': RandomForestClassifier(n_estimators=10
                                                , min_samples_leaf=MIN_SAMPLES)
    }



CONCEPT = 'concept'

def build_ccp_reduction_dataset(alerts_scope: list = None):

    df = build_ds()
    df = df[((df['ccp_diff'] >= 0)
                    | (df['ccp_diff'] < 0))
            & (df.state.isin(['removed']))]
    df[CONCEPT] = df['ccp_diff'].map(lambda x: int(x < 0))

    print("records", len(df))
    print(df[CONCEPT].value_counts(normalize=True))


    df['is_refactor'] = df['is_refactor'].map(lambda x: 1 if x == 1 else 0)
    df['McCabe_sum_reduced'] = df['McCabe_sum_diff'].map(lambda x: bool(x < 0))
    df['McCabe_max_reduced'] = df['McCabe_max_diff'].map(lambda x: bool(x < 0))

    df['only_removal'] = df['added_lines'].map(lambda x: int(x == 0))

    df['mostly_delete'] = df.apply(lambda x: int(x['removed_lines'] > 3*x['added_lines'])
                              , axis=1)
    df['massive_change'] = df.apply(lambda x: int(x['changed_lines'] > 300)
                              , axis=1)

    # To check only complexity alerts
    if alerts_scope:
        df = df[df.alert.isin(alerts_scope)]

    invalid_features = []
    for i in df.columns:
        if df.dtypes[i] not in ('int64', 'float64'):
            invalid_features.append(i)
        elif ('corrective_rate' in i.lower()
                or 'ccp' in i.lower()
                or 'corrective_commits' in i.lower()
                or 'pm' in i.lower()):
            invalid_features.append(i)

    df['high_ccp_group'] = df['ccp_pm_before'].map(lambda x: int(x > 0.39))

    for i in ['McCabe_sum_before', 'McCabe_max_before', 'McCabe_sum_diff', 'McCabe_max_diff']:
        q75 = df[i].quantile(0.75)
        print(i, q75)
        df['high_' + i] = df[i].map(lambda x: int(x > q75))

    for i in df['alert'].unique():
        df[i] = df['alert'].map(lambda x: int(x==i))

    print("nonnumeric_features", invalid_features)
    valid_columns = list(set(df.columns) - set(invalid_features))
    print("valid_columns", valid_columns)

    hand_crafted_features = list(df.alert.unique()) + ['is_refactor'
        , 'McCabe_sum_reduced', 'McCabe_max_reduced', 'only_removal', 'mostly_delete'
        , 'massive_change','high_ccp_group'] + [CONCEPT]
    # df = df[hand_crafted_features]
    df = df[valid_columns]
    df = df.fillna(0)


    return df

def model_ccp_reduction():

    df = build_ccp_reduction_dataset()
    """
    results = build_and_eval_models(df=df
                          , classifiers=classifiers
                          , concept=CONCEPT
                          , test_size=0.3
                          , random_state=343439)

    results_df = save_performance(results)
    print(results_df)
    """
    build_models(df=df
                    , classifiers=classifiers
                    , concept=CONCEPT
                    , test_size=0.3
                    , random_state=343439
                    , performance_path=PERFORMANCE_PATH
                    , models_path=MODELS_PATH
                    , models_format='{model_name}.pkl'
                    , models_text_format='{model_name}.sql'
                    )

def compute_feature_stats():
    df = build_ccp_reduction_dataset()

    # Get confusion metrics for metrics
    stats = pair_features_vs_concept(df=df
                             , features=set(df.columns) - set([CONCEPT])
                             , concept=CONCEPT
                             , metrics=None
                             , verbose=True)
    df = features_stats_to_cm_df(stats)

    df.to_csv(join(PERFORMANCE_DIR
                   , 'ccp_reduction_features_stats.csv'))


def compute_extraction_feature_stats():
    df = build_ccp_reduction_dataset(alerts_scope=extraction_candidates)

    # Get confusion metrics for metrics
    stats = pair_features_vs_concept(df=df
                             , features=set(df.columns) - set([CONCEPT])
                             , concept=CONCEPT
                             , metrics=None
                             , verbose=True)
    df = features_stats_to_cm_df(stats)

    df.to_csv(join(PERFORMANCE_DIR
                   , 'extraction_ccp_reduction_features_stats.csv'))

if __name__ == '__main__':
    #model_ccp_reduction()
    #compute_feature_stats()
    compute_extraction_feature_stats()

