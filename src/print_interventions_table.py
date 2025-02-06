# PATCHING analysis utils
# https://github.com/evidencebp/analysis_utils
import sys

import numpy as np

ANALYSIS_PATH = r'c:\src\analysis_utils'
sys.path.append(ANALYSIS_PATH)

import pandas as pd

from analysis_utils.df_to_latex_table import df_to_latex_table
from interventions_stats import DONE_INTERVENTIONS_STATS
from compute_code_metrics import INTERVENTIONS_CODE_METRICS_STATS

def print_interventions_table():

    description_dict = {'broad-exception-caught': 'Catch Exception, might hide unintended exceptions'
        , 'comparison-of-constants': 'An comparison whose result is known, since side are constant. Usually a bug'
        , 'line-too-long': 'Might hide important code'
        , 'pointless-statement': 'Usually unintended'
        , 'simplifiable-if-expression': 'True if cond else False, equivalent to cond'
        , 'simplifiable-if-statement': 'As the expression yet with a full if'
        , 'superfluous-parens': 'Unneeded extra parenthesis, common in return statements and conditions. \cite{zampetti2022using,amit2021follow}'
        , 'too-many-boolean-expressions': 'An if with many terms'
        , 'too-many-branches': 'A function/method with too many if statements'
        , 'too-many-lines': 'A file with too many lines'
        , 'too-many-nested-blocks': 'A function/method with too high nesting level \cite{zhang2018automated, lenarduzzi2020sonarqube, amit2021follow}'
        ,'too-many-return-statements': 'A function/method with too return statements'
        , 'too-many-statements': 'A function/method with too many lines'
        , 'try-except-raise': 'Might be a useless error handling'
        , 'unnecessary-pass': 'Sometimes a useless statement, many time an empty class'
        , 'using-constant-test': 'An if whose result is known. Usually a bug'
       , 'wildcard-import': 'Import *. Leads to unclear source and possible future collisions \cite{kery2016examining, bestPractices, lenarduzzi2020sonarqube, amit2021follow}'
                        }

    done_df = pd.read_csv(DONE_INTERVENTIONS_STATS)
    metrics_df = pd.read_csv(INTERVENTIONS_CODE_METRICS_STATS)

    table_df = pd.merge(done_df[['msg_id', 'msg', 'alerts', 'repositories', 'merged_alerts']]
                     , metrics_df[['msg_id', 'modified_McCabe_max_diff', 'SLOC_diff', 'McCabe_sum_diff']]
                     , on='msg_id'
                     , how='left')
    table_df.sort_values('msg'
                      , inplace=True)
    table_df['Description'] = table_df['msg'].map(lambda x: description_dict[x])
    table_df.rename(columns={'msg': 'Alert'
                             , 'alerts': 'Alerts'
                             , 'repositories': 'Repositories'
                             , 'merged_alerts': 'Merged'
                             , 'modified_McCabe_max_diff': 'McCabe Max'
                             , 'SLOC_diff': 'LOC'
                             , 'McCabe_sum_diff': 'McCabe Sum'}

                    , inplace=True)

    for i in ['Alerts', 'Repositories', 'Merged']:
        table_df[i] = table_df[i].map(lambda x: ''  if np.isnan(x) else str(int(x)) + ' ')

    table_df.fillna(''
                    , inplace=True)

    title = ' \label{tab:alerts} Interventions Code Metrics Difference'
    print()
    df_to_latex_table(
        table_df[['Alert', 'Description', 'Alerts', 'Merged', 'Repositories',  'McCabe Max', 'McCabe Sum', 'LOC']]
        , title
        , rounding_digits=1)
    print()


if __name__ == "__main__":
    print_interventions_table()
