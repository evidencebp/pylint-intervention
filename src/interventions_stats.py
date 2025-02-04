from os import listdir
from os.path import join

import pandas as pd

from configuration import BASE_DIR, DONE_DIRECTORY, PR_COL, HARMFUL_COL, BENEFIT_COL, REPO_COL

NUM_HARMFUL_COL = 'Is harmful?'

DONE_INTERVENTIONS_STATS = join(BASE_DIR
                                , 'interventions'
                                , 'all_done_interventions_stats.csv')


def get_all_interventions():

    intervention_files = listdir(DONE_DIRECTORY)

    dfs = []
    for i in intervention_files:
        df = pd.read_csv(join(DONE_DIRECTORY
                              , i))
        df['file'] = i
        dfs.append(df)

    all_df = pd.concat(dfs)

    return all_df

def interventions_stats():
    all = get_all_interventions()

    all[BENEFIT_COL] = all[BENEFIT_COL].map(lambda x: None if not str(x).isnumeric() or x == ' ' else int(x))
    all.to_csv(join(BASE_DIR
                    , 'interventions'
                    , 'all_done_interventions.csv')
               , index=False)

    if not set(all[HARMFUL_COL].unique()).issubset(set(['No', 'Yes', ' ', 'Partial'])):
        print("Unexpected harmfulness")
        print(all[HARMFUL_COL].unique())
    all[NUM_HARMFUL_COL] = all[HARMFUL_COL].map(lambda x: 1 if x == 'Yes' else 0)
    all["Won't fix"] = all[PR_COL].map(lambda x: 1 if x == "Won’t fix" else 0)
    all["Owner objection"] = all[PR_COL].map(lambda x: 1 if x == "owner objected" else 0)
    all['msg'] = all['msg'].map(lambda x: x.replace(' ', ''))

    performed = all[(all.chosen == 1)
                        & (all[PR_COL].notna())]

    g = performed.groupby(['msg_id',	'msg']
                          , as_index=False).agg(alerts=('alerts', lambda x: sum(x))
                                                 , repositories=(REPO_COL, 'nunique')
                                                 , benefit = (BENEFIT_COL, 'mean')
                                                 , harmfulness=(NUM_HARMFUL_COL, 'mean')
                                                 , will_not_fix=("Won't fix", 'mean')
                                                 , owner_objection=("Owner objection", 'mean')
                                                 )
    merged_interventions = get_merged_interventions()
    g = pd.merge(g
                 , merged_interventions
                 , on=['msg_id',	'msg']
                 , how='left')

    g.to_csv(DONE_INTERVENTIONS_STATS
               , index=False)

def get_merged_interventions():
    all_df = pd.read_csv(join(BASE_DIR
                    , 'interventions'
                    , 'all_done_interventions.csv'))
    repos_df = pd.read_csv(join(BASE_DIR
                    , 'interventions'
                    , 'repositories.csv'))
    joint = pd.merge(all_df
                     , repos_df
                     , left_on=PR_COL
                     , right_on='pr')
    joint = joint[joint['status'] == 'merged']
    joint['msg'] = joint['msg'].map(lambda x: x.replace(' ', ''))

    g = joint.groupby(['msg_id',	'msg']
                          , as_index=False).agg(merged_alerts=('alerts', lambda x: sum(x))
                                                 , merged_repositories=(REPO_COL, 'nunique')
                                                 )
    return g

if __name__ == "__main__":
    interventions_stats()
