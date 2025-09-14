import os
import sys

from analysis_utils.analysis_utils.df_to_latex_table import df_to_latex_table

ANALYSIS_PATH = r'c:\src'
sys.path.append(ANALYSIS_PATH)

from analysis_utils.analysis_utils.ml_utils import build_and_eval_models, save_performance, build_models
from analysis_utils.analysis_utils.feature_pair_analysis import pair_features_vs_concept, features_stats_to_cm_df

from configuration import BASE_DIR
from compute_commit_profile import extraction_candidates
from analyze_process_metrics import build_ds

PERFORMANCE_DIR = os.path.join(BASE_DIR
                                , r'performance')
PERFORMANCE_PATH = os.path.join(PERFORMANCE_DIR
                                , 'ccp_reduction_cm_w3_1.csv')
MODELS_PATH = os.path.join(BASE_DIR, r'models')

from os.path import join
import numpy as np
import pandas as pd

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

class_weight = {1: 3, 0: 1}

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


classifiers = {'Tree_ms_md': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                                       , max_depth=MAX_DEPTH
                                                       , class_weight=class_weight)
    , 'Tree_default': DecisionTreeClassifier(class_weight=class_weight)
    , 'Tree_ms': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                          , class_weight=class_weight)
    , 'Tree_md': DecisionTreeClassifier(max_depth=MAX_DEPTH
                                         , class_weight=class_weight)
    , 'RandomForest': RandomForestClassifier(n_estimators=10
                                             , min_samples_leaf=MIN_SAMPLES)
               }

large_classifiers = {'Tree_ms50_md3': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                                             , max_depth=MAX_DEPTH
                                                             , class_weight=class_weight)
    , 'Tree_default': DecisionTreeClassifier(class_weight=class_weight)
    , 'Tree_ms50': DecisionTreeClassifier(min_samples_leaf=MIN_SAMPLES
                                          , class_weight=class_weight)
    , 'Tree_md3': DecisionTreeClassifier(max_depth=MAX_DEPTH
                                         , class_weight=class_weight)
    , 'RandomForest': RandomForestClassifier(n_estimators=10
                                             , min_samples_leaf=MIN_SAMPLES)
    , 'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=0, learning_rate=0.1)
    , 'AdaBoost_n_small': AdaBoostClassifier(n_estimators=30, random_state=0, learning_rate=0.1)
    #, 'AdaBoost_base_small': AdaBoostClassifier(base_estimator=base
    #                                             , n_estimators=50, random_state=0, learning_rate=0.1)
    #, 'AdaBoost_v1': AdaBoostClassifier(base_estimator=base
    #                                    , n_estimators=100, random_state=0, learning_rate=0.1)
    , 'GradientBoostingClassifier': GradientBoostingClassifier(learning_rate=0.1
                                                                , min_samples_leaf=MIN_SAMPLES
                                                                , max_depth=MAX_DEPTH)
    , 'Stump': DecisionTreeClassifier(max_depth=1
                                      , class_weight=class_weight)
    , 'LogisticRegression': LogisticRegression(class_weight=class_weight, max_iter=1000)
     , 'SVC': SVC()
    , 'SGDClassifier': SGDClassifier()
    # , 'KNeighborsClassifier': KNeighborsClassifier()
                     # , 'MultinomialNB': MultinomialNB()
    , 'MLPClassifier': MLPClassifier(solver='lbfgs', alpha=1e-5,
                                      hidden_layer_sizes=(5, 2), random_state=1, max_iter=20000)

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
    df['low_ccp_group'] = df['ccp_pm_before'].map(lambda x: int(x < 0.09))

    for i in ['McCabe_sum_before', 'McCabe_max_before', 'McCabe_sum_diff', 'McCabe_max_diff']:
        q75 = df[i].quantile(0.75)
        print(i, q75)
        df['high_' + i] = df[i].map(lambda x: int(x > q75))

    for i in ['McCabe_sum_before', 'McCabe_max_before', 'McCabe_sum_diff', 'McCabe_max_diff']:
        q25 = df[i].quantile(0.25)
        print(i, q25)
        df['low_' + i] = df[i].map(lambda x: int(x < q25))

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
                    , classifiers=large_classifiers
                    , concept=CONCEPT
                    , test_size=0.3
                    , random_state=343439
                    , performance_path=PERFORMANCE_PATH
                    , models_path=MODELS_PATH
                    , models_format='{model_name}.pkl'
                    , models_text_format='{model_name}.sql'
                    )

def compute_feature_stats(alerts_scope
                          , output):
    df = build_ccp_reduction_dataset(alerts_scope=extraction_candidates)

    # Get confusion metrics for metrics
    stats = pair_features_vs_concept(df=df
                             , features=set(df.columns) - set([CONCEPT])
                             , concept=CONCEPT
                             , metrics=None
                             , verbose=True)
    df = features_stats_to_cm_df(stats)
    df = df.reset_index().rename(columns={'index': 'Feature'})

    if output:
        df.to_csv(output
                  , index=False)

    return df



def print_features_stats(df):

    df.rename(columns={'accuracy': 'Accuracy'
                        , 'hit_rate': 'Hit Rate'
                        , 'precision': 'Precision'
                        , 'precision_lift': 'Precision Lift'
                        , 'recall': 'Recall'}
              , errors='raise'
              , inplace=True)
    df = df[~df.Feature.isin(['volume_diff', 'effort_diff',
       'bugs_diff', 'time_diff', 'cur_count_x', 'calculated_length_diff',
       'cur_count', 'cur_count_y', 'difficulty_diff'])]
    df['Feature'] = df['Feature'].map(lambda x: x.replace('_', ' '))
    df_to_latex_table(df[['Feature', 'Accuracy', 'Hit Rate', 'Precision', 'Precision Lift', 'Recall']]
                        , caption=' \label{tab:features-cm} Features Predictive Performance'
                        , columns_to_name=None
                        , star_table=True
                        , columns_header=None)


def main():
    model_ccp_reduction()
    #compute_feature_stats(alerts_scope=None
    #                      , output=join(PERFORMANCE_DIR
    #               , 'ccp_reduction_features_stats.csv'))

    df = compute_feature_stats(alerts_scope=extraction_candidates
                          , output=join(PERFORMANCE_DIR
                   , 'extraction_ccp_reduction_features_stats.csv'))
    print_features_stats(df)

if __name__ == '__main__':
    main()

