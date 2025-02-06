"""
See
https://radon.readthedocs.io/en/latest/index.html

"""
from os.path import join
import numpy as np
import pandas as pd

from configuration import METRICS_BEFORE_DIR, METRICS_AFTER_DIR, REPO_COL
from utils import run_powershell_cmd, get_project_name, encode_path, get_done_interventions


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

def get_raw_metrics(file: str)-> dict:

    return get_metrics_set(file
                    , type='raw'
                    , metric_to_extract=['LOC', 'LLOC', 'SLOC', 'Comments', 'Single comments', 'Multi', 'Blank'])

def get_Halstead_metrics(file: str)-> dict:
    return get_metrics_set(file
                    , type='hal'
                    , metric_to_extract=['h1', 'h2', 'N1', 'N2', 'vocabulary', 'length', 'calculated_length'
                                         , 'volume', 'difficulty', 'effort', 'time', 'bugs'])

def get_McCabe_complexity(file:str) -> pd.DataFrame:
    cmd = f'radon  cc -s  {file}'

    result = str(run_powershell_cmd(cmd).stdout)
    result = result[result.find('\\r\\n'):] # Skipping file name

    if 'ERROR' in result:
        print("Error in computing McCabe complexity ", file)
        df = pd.DataFrame([[file, None, None]]
                          , columns=['file', 'name', 'complexity'])
    else:
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
    metrics['McCabe_max'] = McCabe['complexity'].max()
    metrics['McCabe_sum'] = McCabe['complexity'].max() if np.isnan(McCabe['complexity'].max()) else McCabe['complexity'].sum()

    df = pd.DataFrame(metrics, index=[0])

    return df

def get_relevant_McCabe_stats(repo_name
                              , source_file):

    metrics = {'repo_name': repo_name
               , 'path': source_file}

    McCabe_path = join(METRICS_BEFORE_DIR
                       , 'McCabe'
                       , get_project_name(repo_name))
    McCabe_file = join(McCabe_path
                       , encode_path(source_file).replace('.py', '.csv'))
    before_df = pd.read_csv(McCabe_file)

    McCabe_path = join(METRICS_AFTER_DIR
                       , 'McCabe'
                       , get_project_name(repo_name))
    McCabe_file = join(McCabe_path
                       , encode_path(source_file).replace('.py', '.csv'))
    after_df = pd.read_csv(McCabe_file)


    joint = pd.merge(after_df[['name', 'complexity']]
                        , before_df[['name', 'complexity']]
                        , on=['name']
                        #, how='left'
                        , suffixes=('_after', '_before'))
    joint = joint[(joint['complexity_before'] != joint['complexity_after'])]
    if len(joint):
        """
        joint['complexity_before'] = joint['complexity_before'].map(lambda x: 0 if np.isnan(x) else x)
        joint['diff'] = joint.apply(lambda x: x['complexity_after'] - x['complexity_before']
                                    , axis=1)
        """
        metrics['modified_McCabe_max_diff'] = joint['complexity_after'].max() - joint['complexity_before'].max()

        """
        complexity_before_sum = (joint['complexity_before'].max() if np.isnan(joint['complexity_before'].max())
                                 else joint['complexity_before'].sum())
        complexity_after_sum = (joint['complexity_after'].max() if np.isnan(joint['complexity_after'].max())
                                 else joint['complexity_after'].sum())

        metrics['modified_McCabe_sum_diff'] = complexity_after_sum - complexity_before_sum
        """
    else:
        metrics['modified_McCabe_max_diff'] = None
        #metrics['modified_McCabe_sum_diff'] = None

    df = pd.DataFrame(metrics, index=[0])

    return df

def get_repo_relevant_McCabe_stats(interventions_file):
    df = get_done_interventions(interventions_file)

    repo_name = df[REPO_COL].astype(str).max() # Should be same value, max takes one

    stats = []
    for source_file in df['path'].unique():
        stat = get_relevant_McCabe_stats(repo_name
                              , source_file)
        stats.append(stat)

    stats_df = pd.concat(stats)

    return stats_df

