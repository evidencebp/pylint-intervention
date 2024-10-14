from os import listdir
from os.path import join
import datetime


import pandas as pd

from configuration import BASE_DIR

def get_candidate_stats(file_name: str
                        , interventions_df: pd.DataFrame
                        , alerts_df: pd.DataFrame) -> pd.DataFrame:

    stats_dict = {}
    stats_dict['file_name'] = file_name
    stats_dict['time'] = datetime.datetime.now()
    stats_dict['alerts'] =  len(interventions_df)
    stats_dict['interventions'] = len(interventions_df[interventions_df['chosen'] == 1])
    stats_dict['intervention_types'] = interventions_df[interventions_df['chosen'] == 1]['msg_id'].nunique()

    for _, i in alerts_df.iterrows():
        stats_dict[i['msg']] =  len(interventions_df[(interventions_df['chosen'] == 1)
                                    & (interventions_df['msg_id'] == i['msg_id'])])

    stats = pd.DataFrame(stats_dict, index=[0])

    return stats

def compute_candidates_stats():

    ALERT_TYPES_FILE = join(BASE_DIR
                            , 'tools/project_analysis/alert_types.csv')

    CANDIDATES_DIR = join(BASE_DIR
                          , 'interventions/candidates/')

    alerts_df = pd.read_csv(ALERT_TYPES_FILE)

    candidates_files = listdir(CANDIDATES_DIR)

    dfs = []
    for i in candidates_files:
        interventions_df = pd.read_csv(join(CANDIDATES_DIR
                              , i))
        stat = get_candidate_stats(file_name=i
                                , interventions_df=interventions_df
                                , alerts_df=alerts_df)
        dfs.append(stat)

    all_df = pd.concat(dfs)

    all_df.to_csv(join(BASE_DIR
                       , 'interventions/candidates_detailed_stats.csv')
                  , index=False)

if __name__ == '__main__':
    compute_candidates_stats()
