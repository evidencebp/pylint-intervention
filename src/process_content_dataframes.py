import os
from os.path import join
import pandas as pd

from configuration import BASE_DIR, CONFIG_FILE, TYPES_FILE
from utils import pylint_analysis, write_file

TEMP_FILE = 'c:/tmp/tmp_content.py'

CHANGES_FILE = join(BASE_DIR
                    , 'data/in_the_wild/changed_alerts.csv')


def process_content_dataframe(df: pd.DataFrame
                              , output_file: str = None):

    types_df = pd.read_csv(TYPES_FILE)

    all_alerts = []
    file_num = 0
    # Go over rows
    for _, i in df.iterrows():
        try:
            file_num = file_num + 1
            # copy content to file
            write_file(output_file=TEMP_FILE
                       ,content=str(i['content']))

            # Analyze file
            alerts = pylint_analysis(target=TEMP_FILE
                        , config=CONFIG_FILE
                        , types=types_df)

            # Add results
            if alerts is not None:
                alerts['repo_name'] = i['repo_name']
                alerts['path'] = i['path']
                all_alerts.append(alerts)

            # Delete temporary content file
            os.remove(TEMP_FILE)
        except Exception as e:
            print("error processing", i['repo_name'], i['path'] )
            print(e)

        if file_num % 100 == 0:
            print(file_num)

    alerts_df = pd.concat(all_alerts)

    # Store results
    if output_file:
        alerts_df.to_csv(output_file
                         , index=False)
    return alerts_df

def process_content_dataframes():

    content_files = ['C:/tmp/aug/code_python_aug_content_aug_22000000000000'
                      , 'C:/tmp/aug/code_python_aug_content_aug_22000000000001'
                      , 'C:/tmp/aug/code_python_aug_content_aug_22000000000002'
                      , 'C:/tmp/aug/code_python_aug_content_aug_22000000000003'
                     ]

    all_alerts = []
    for i in content_files:
        print(i, '**********************')
        df = pd.read_csv(i
                         #, nrows=100 # TODO - remove
                         )
        alerts = process_content_dataframe(df)

        all_alerts.append(alerts)

    alerts_df = pd.concat(all_alerts)
    alerts_df.to_csv('C:/tmp/aug/code_python_aug_alerts.csv'
                         , index=False)

def build_alert_diffs():
    feb_df = pd.read_csv(join(BASE_DIR
                              , 'data/in_the_wild/code_python_feb_alerts.csv'))
    aug_df = pd.read_csv(join(BASE_DIR
                              , 'data/in_the_wild/code_python_aug_alerts.csv'))

    feb_single_alert = feb_df[feb_df['alerts'] == 1]
    removed_alerts = pd.merge(feb_single_alert
                              , aug_df
                              , on=['repo_name', 'path', 'msg_id', 'msg']
                              , how='left'
                              , suffixes=('_feb', '_aug'))
    removed_alerts = removed_alerts[removed_alerts['alerts_aug'].isna()]
    removed_alerts = removed_alerts[['path', 'msg_id', 'msg', 'repo_name']]
    removed_alerts['change'] = 'removed'


    aug_single_alert = aug_df[aug_df['alerts'] == 1]
    added_alerts = pd.merge(aug_single_alert
                              , feb_df
                              , on=['repo_name', 'path', 'msg_id', 'msg']
                              , how='left'
                              , suffixes=('_aug', '_feb'))
    added_alerts = added_alerts[added_alerts['alerts_feb'].isna()]
    added_alerts = added_alerts[['path', 'msg_id', 'msg', 'repo_name']]
    added_alerts['change'] = 'added'
    
    changed_alerts = pd.concat([removed_alerts
                                , added_alerts])
    changed_alerts.to_csv(CHANGES_FILE
                          , index=False)


def change_stats():
    df = pd.read_csv(CHANGES_FILE)
    print(df.msg.value_counts().sort_index())

    g = df[df['change']=='removed'].groupby(
        ['msg']
        , as_index=False).agg({'repo_name': 'nunique'
                            , 'path': 'nunique'}).sort_values(['msg'])
    print(g)

    print("repos of interest"
          , df[(df['change']=='removed')
                & (df.msg.isin(['simplifiable-if-expression'
                                   , 'simplifiable-if-statement']))].repo_name.nunique())

if __name__ == "__main__":
    #process_content_dataframes()
    #build_alert_diffs()
    change_stats()
