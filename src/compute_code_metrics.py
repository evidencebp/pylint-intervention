"""

Getting code metrics using Radon
https://radon.readthedocs.io/en/latest/index.html
"""
from os import listdir

from os.path import join
import pandas as pd

from configuration import DONE_DIRECTORY, PROJECTS_DIR, PR_COL, REPO_COL
from utils import run_powershell_cmd, get_project_name

def get_raw_metrics(file: str)-> dict:

    return get_metrics_set(file
                    , type='raw'
                    , metric_to_extract=['LOC', 'LLOC', 'SLOC', 'Comments', 'Single comments', 'Multi', 'Blank'])

def get_Halstead_metrics(file: str)-> dict:
    return get_metrics_set(file
                    , type='hal'
                    , metric_to_extract=['h1', 'h2', 'N1', 'N2', 'vocabulary', 'length', 'calculated_length'
                                         , 'volume', 'difficulty', 'effort', 'time', 'bugs'])

def get_metrics_set(file: str
                    , type:str
                    , metric_to_extract)-> dict:

    metrics_dict = {}
    cmd = f'radon {type} {file}'

    result = str(run_powershell_cmd(cmd).stdout)

    for i in metric_to_extract:
        i_pos = result.find(i)
        metrics_dict[i] = result[i_pos
                                     + len(i)
                                     +2 # for ': '
                                     : result.find('\\r\\n', i_pos)]
    return metrics_dict

def get_McCabe_complexity(file:str) -> pd.DataFrame:
    cmd = f'radon  cc -s  {file}'

    result = str(run_powershell_cmd(cmd).stdout)
    result = result[result.find('\\r\\n'):] # Skipping file name

    rows = []
    while result.find(":") != -1:
        start = result.find(":")
        start = result.find(" ", start)
        name = result[start+1:result.find(" ", start+1)]

        # getting complexity
        result = result[start:]
        start = result.find("(")
        end = result.find(")")
        complexity = int(result[start+1: end])
        result = result[end+1:]

        rows.append((file, name, complexity))

    df = pd.DataFrame(rows
                      , columns=['file', 'name', 'complexity'])

    return df

def analyze_file(file: str):

    metrics = get_raw_metrics(file)
    metrics.update(get_Halstead_metrics(file))
    McCabe = get_McCabe_complexity(file)
    metrics['McCabe_mean'] = McCabe['complexity'].mean()
    metrics['McCabe_sum'] = McCabe['complexity'].sum()
    metrics['McCabe_max'] = McCabe['complexity'].max()

    df = pd.DataFrame(metrics, index=[0])

    return df

def get_current_repo_metrics(interventions_file):
    df = pd.read_csv(interventions_file)
    df = df[~df[PR_COL].isna()]
    df = df[df[PR_COL].str.contains('github')]

    metrics_list = []
    for _, i in df.iterrows():
        repo_name = i[REPO_COL]
        metrics = analyze_file(join(PROJECTS_DIR
                                , get_project_name(repo_name)
                                , i.path))
        metrics['path'] = i.path
        metrics_list.append(metrics)

    metrics_df = pd.concat(metrics_list)
    metrics_df.to_csv(join("C:/src/pylint-intervention/data/code_metrics/after/"
                           , repo_name.replace("/", "_slash_") + ".csv")
                      , index=False)


def get_all_current_repo_metrics():

    intervention_files = listdir(DONE_DIRECTORY)

    for i in intervention_files:
        print(i)
        get_current_repo_metrics(join(DONE_DIRECTORY
                              , i))

#interventions_file = "C:/src/pylint-intervention/interventions/done/mralext20_alex-bot_interventions_October_05_2024.csv"
#get_current_repo_metrics(interventions_file)
get_all_current_repo_metrics()
#print(analyze_file("C:/src/alex-bot/alexBot/cogs/voiceCommands.py"))