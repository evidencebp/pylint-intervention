import os
from datetime import date
import random

import pandas as pd

AGG_ALERTS_FILE = "interventions.csv"


def get_alerts():
    ALERTS_FILE = "alerts.csv"

    # get alerts
    PYLINT_CMD = "pylint  --rcfile=pylint_short.cfg --score=n" \
                 + " --msg-template='{path},{line},{msg_id}' . >  " \
                 + ALERTS_FILE
    alerts = os.system(PYLINT_CMD)
    lines = count_file_lines(ALERTS_FILE)
    if lines:
        df = pd.read_csv(ALERTS_FILE, skiprows=1, header=None)

        # aggregate alerts
        df.columns = ['path', 'line', 'msg_id']
        types = pd.read_csv("alert_types.csv")
        df = pd.merge(df
                      , types
                      , on='msg_id'
                      , how='left')

        df = df[df['path'].notna()
                & df['line'].notna()
                & df['msg_id'].notna()
                & df['msg'].notna()]  # Filter out bad parsing
        agg = df.groupby(['path', 'msg_id']
                         , as_index=False).agg({'line': 'count'
                                                   , 'msg': 'max'})  # Message is similar
        # , max chooses one
        agg.rename(columns={'line': 'alerts'}
                   , inplace=True)
    else:
        os.remove(ALERTS_FILE)
        agg = None

    return agg


def filterout_tests(df: pd.DataFrame):
    return df[~df['path'].str.contains("test", case=False)]


def file_split(path: str) -> str:
    loc = path.rfind("/")
    if loc == -1:
        name = path
    else:
        name = path[loc + 1:]

    return int(bin(hash(name))[-1])


def train_test_split(df: pd.DataFrame) -> pd.DataFrame:
    df['can_intervene'] = df['path'].map(file_split)

    return df


def select_alert_to_fix(df: pd.DataFrame) -> pd.DataFrame:
    df['chosen'] = 0
    for file in df['path'].unique():
        alerts = df[(df['path'] == file)
                    & (df['alerts'] < 3)]['msg_id'].unique()
        if len(alerts) > 0:
            chosen = random.choice(alerts)
            df['chosen'] = df.apply(
                lambda x: 1 if (x['path'] == file and x['msg_id'] == chosen) else x['chosen']
                , axis=1)

    # Get a pseudo random file order, avoiding working by directory structure
    df['order'] = df['path'].map(lambda x: int(bin(hash(x))[4:10]))
    df = df.sort_values(['chosen', 'order', 'path'], ascending=[False, True, True])
    df.drop(columns=['order']
            , inplace=True)

    return df


def get_commits(file: str) -> int:
    TEMP_FILE = "commits.txt"

    cmd = " git log --format=%H --since=90.days {file} > {temp} ".format(file=file
                                                                         , temp=TEMP_FILE)
    os.system(cmd)
    lines = count_file_lines(TEMP_FILE)

    os.system("del " + TEMP_FILE)

    return lines


def count_file_lines(file):
    with open(file, 'r') as fp:
        lines = len(fp.readlines())
    return lines


def enhance_with_git_history(df: pd.DataFrame) -> pd.DataFrame:
    df['90_days_commits'] = df['path'].map(get_commits)

    return df


def make_convenient(df: pd.DataFrame) -> pd.DataFrame:
    df = df[['path', 'msg_id', 'msg', 'alerts', 'chosen']]

    df['In which repository the modification was done?'] = ' '
    df['In which pull request the modification was done?'] = ' '
    df['Do you consider the removed alert harmful?'] = ' '
    df['Why do you consider it harmful (or harmless)?'] = ' '
    df['What is the code quality (1 lowest, 10 best)?' \
       + ' Code quality refers to the code prior to the pull request.'] = ' '
    df['Why do you consider the code quality as such?'] = ' '
    df['What is the expected benefit(1 – negative, 5 – neutral, 10 – great)?'] = ' '
    df['Why do you consider the pull request to improve the code (or not improve it)?'] = ' '

    return df


def analyze():
    alerts = get_alerts()

    if alerts is not None:
        alerts = filterout_tests(alerts)
        alerts = train_test_split(alerts)
        alerts = select_alert_to_fix(alerts)
        alerts = enhance_with_git_history(alerts)
        alerts = make_convenient(alerts)

        today = date.today()
        #alerts.to_csv(AGG_ALERTS_FILE.format(date=today.strftime("%B_%d_%Y"))
        alerts.to_csv(AGG_ALERTS_FILE
                      , index=False)
    else:
        print("No alerts were found.")


if __name__ == "__main__":
    analyze()
