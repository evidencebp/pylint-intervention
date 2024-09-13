import os
import random

import pandas as pd

AGG_ALERTS_FILE = "interventions.txt"


def get_alerts():

    ALERTS_FILE = "alerts.txt"

    # get alerts
    PYLINT_CMD = "pylint  --rcfile=pylint_short.cfg --score=n --msg-template='{path},{line},{msg_id}' . >  " + ALERTS_FILE
    alerts = os.system(PYLINT_CMD)
    df = pd.read_csv(ALERTS_FILE, skiprows=1, header=None)

    # aggregate alerts
    df.columns = ['path', 'line', 'msg_id']
    agg = df.groupby(['path', 'msg_id']
                     , as_index=False).agg({'line': 'count'})
    agg.rename(columns={'line': 'alerts'}
               , inplace=True)

    return agg

def filterout_tests(df: pd.DataFrame):
    return df[~df['path'].str.contains("test", case=False)]

def file_split(path: str) -> str:

    loc = path.rfind("/")
    if loc == -1:
        name = path
    else:
        name = path[loc+1:]

    return int(bin(hash(name))[-1])



def train_test_split(df: pd.DataFrame) -> pd.DataFrame:
    df['can_intervene'] = df['path'].map(file_split)

    return df

def select_alert_to_fix(df: pd.DataFrame) -> pd.DataFrame:

    df['chosen'] = 0
    for file in df['path'].unique():
        alerts = df[(df['path'] == file)
                    & (df['alerts'] < 3)]['msg_id'].unique()
        chosen = random.choice(alerts)
        df['chosen'] = df.apply(lambda x: 1 if (x['path'] == file and x['msg_id'] == chosen) else x['chosen']
                                          , axis=1)

    return df

def analyze():
    alerts = get_alerts()
    alerts = filterout_tests(alerts)
    alerts = train_test_split(alerts)
    alerts = select_alert_to_fix(alerts)

    alerts.to_csv(AGG_ALERTS_FILE
               , index=False)

if __name__ == "__main__":
    analyze()