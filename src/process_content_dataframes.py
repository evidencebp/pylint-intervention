import os
from os.path import join
import pandas as pd

from configuration import BASE_DIR
from utils import pylint_analysis, write_file

TEMP_FILE = 'c:/tmp/tmp_content.py'
CONFIG_FILE = join(BASE_DIR
                    , "tools/project_analysis/pylint_short.cfg")
TYPES_FILE = join(BASE_DIR
                    , "tools/project_analysis/alert_types.csv")

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


if __name__ == "__main__":
    process_content_dataframes()
