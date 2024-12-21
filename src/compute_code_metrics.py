"""

Getting code metrics using Radon
https://radon.readthedocs.io/en/latest/index.html
"""
import datetime
from os import listdir

from os.path import join
import numpy as np
import pandas as pd

from configuration import BASE_DIR, DONE_DIRECTORY, PROJECTS_DIR, PR_COL, REPO_COL
from utils import run_powershell_cmd, get_project_name, get_file_prev_commit, show_file_content

BEFORE_DIR = join(BASE_DIR
                    , "data/code_metrics/before/")
AFTER_DIR = join(BASE_DIR
                    , "data/code_metrics/after/")

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
        try:
            complexity = int(result[start+1: end])
        except:
            print("Error parsing complexity", file)
            complexity = None
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

def get_metrics_file(repo_name):
    return repo_name.replace("/", "_slash_") + ".csv"

def get_repo_metrics(interventions_file
                             , current=True
                             , verbose=False):
    df = pd.read_csv(interventions_file)
    df = df[~df[PR_COL].isna()]
    df = df[df[PR_COL].str.contains('github')]

    metrics_list = []
    for _, i in df.iterrows():
        if verbose:
            print(datetime.datetime.now(), "analyzing ", i['path'])
        repo_name = i[REPO_COL]
        repo_dir = join(PROJECTS_DIR
                        , get_project_name(repo_name))
        if not current:
            first_intervention_commit = get_author_first_commit_in_repo(repo_dir=repo_dir)
            pre_intervention_commit = get_file_prev_commit(commit=first_intervention_commit
                                                           ,repo_dir=repo_dir)
            tmp_file = join(BASE_DIR
                                                 , 'tmp.py')
            show_file_content(i.path
                              , repo_dir
                              , commit=pre_intervention_commit
                              , output_file=tmp_file)
            metrics = analyze_file(tmp_file)
            metrics['commit'] = pre_intervention_commit
        else:

            metrics = analyze_file(join(repo_dir
                                , i.path))
        metrics['path'] = i.path

        if np.isreal(metrics['LOC']): # Avoid failure to analyze
            metrics_list.append(metrics)

    metrics_df = pd.concat(metrics_list)

    if current:
        metrics_df.to_csv(join(AFTER_DIR
                           , get_metrics_file(repo_name))
                      , index=False)
    else:
        metrics_df.to_csv(join(BEFORE_DIR
                           , get_metrics_file(repo_name))
                      , index=False)


def get_all_repo_metrics(current=True):

    EXCLUDED_REPOS= ['aajanki_yle-dl_interventions_October_06_2024.csv'] # For some reason computation takes too long
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)


    for i in intervention_files:
        print(datetime.datetime.now(), i)
        get_repo_metrics(join(DONE_DIRECTORY
                              , i)
                                , current=current
                                , verbose=True)

def get_author_first_commit_in_repo(repo_dir: str
                                    , author_name: str = "evidencebp"):
    # git log --author=evidencebp --format='format: %H'
    cmd = f"cd {repo_dir};   git log --author={author_name} --format='format: %H'"
    result = run_powershell_cmd(cmd)

    commit = str(result.stdout)
    commit = commit[commit.rfind("\\n") + 3:-1] # +3 due to "\\n ", -1 due to ending '

    return commit

def compute_code_differences():
    KEY= 'path'

    intervention_files = listdir(DONE_DIRECTORY)
    EXCLUDED_REPOS= ['aajanki_yle-dl_interventions_October_06_2024.csv'] # For some reason computation takes too long
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    all_metrics = []
    for i in intervention_files:
        print(datetime.datetime.now(), i)

        intervention_df = pd.read_csv(join(DONE_DIRECTORY
                                           , i))
        intervention_df = intervention_df[~intervention_df[PR_COL].isna()]
        intervention_df = intervention_df[intervention_df[PR_COL].str.contains('github')]

        repo_name = intervention_df[REPO_COL].max()
        try:
            before_df = pd.read_csv(join(BEFORE_DIR
                                               , get_metrics_file(repo_name)))
            after_df = pd.read_csv(join(AFTER_DIR
                                               , get_metrics_file(repo_name)))
            metrics = pd.merge(before_df
                               , after_df
                               , on=KEY
                               , suffixes=('_before', '_after'))
            aggs = {'path': 'count'
                , 'msg': 'max'}
            for c in set(before_df.columns) - set([KEY, 'commit'
                                                   , 'McCabe_max_diff', 'McCabe_mean_diff', 'McCabe_sum_diff']): # TODO - return McCabe
                try:
                    metrics['tmp'] = metrics[c + '_before'].map(lambda x: None if 'ERROR' in x else float(x))
                    metrics[c + '_diff'] = metrics[c + '_after'] - metrics['tmp']
                    #metrics[c + '_diff'] = metrics.apply(
                    #    lambda x: None if ('ERROR' in str([c + '_before'])) else x[c + '_after'] - x[c + '_before']
                    #    , axis=1
                    #)
                except TypeError:
                    print("Type error in", c, i)
                    metrics[c + '_diff'] = None
                aggs[c + '_diff'] = 'mean'

            joint = pd.merge(intervention_df
                             , metrics
                             , on=KEY)
            all_metrics.append(joint)

        except FileNotFoundError:
            print("A file was not found", i)

    all_metrics_df = pd.concat(all_metrics)
    all_metrics_df.to_csv(join(BASE_DIR
                            , 'interventions/interventions_code_metrics.csv')
                       , index=False)

    g = all_metrics_df.groupby(['msg_id']
                            , as_index=False).agg(aggs)
    g.to_csv(join(BASE_DIR
                            , 'interventions/interventions_code_metrics_stats.csv'))

#interventions_file = "C:/src/pylint-intervention/interventions/done/mralext20_alex-bot_interventions_October_05_2024.csv"
#get_current_repo_metrics(interventions_file)
#get_all_current_repo_metrics()
#print(analyze_file("C:/src/alex-bot/alexBot/cogs/voiceCommands.py"))

#print(get_author_first_commit_in_repo("c:/interventions/alex-bot"))
"""
print(get_file_prev_commit(commit="0a6d54251d775b5111117de430683e2b6e7c3cb3"
                           , repo_dir="c:/interventions/alex-bot"))
print(show_file_content(file_name="alexBot\cogs\\reminders.py"
                            , repo_dir="c:/interventions/alex-bot"
                            , commit=get_file_prev_commit(commit="0a6d54251d775b5111117de430683e2b6e7c3cb3"
                           , repo_dir="c:/interventions/alex-bot")))
"""
#get_all_repo_metrics(current=False)
compute_code_differences()
