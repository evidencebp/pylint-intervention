import numpy as np
import pandas as pd

from utils import run_powershell_cmd


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
    metrics['McCabe_mean'] = McCabe['complexity'].mean()
    metrics['McCabe_max'] = McCabe['complexity'].max()
    metrics['McCabe_sum'] = McCabe['complexity'].max() if np.isnan(McCabe['complexity'].max()) else McCabe['complexity'].sum()

    df = pd.DataFrame(metrics, index=[0])

    return df
