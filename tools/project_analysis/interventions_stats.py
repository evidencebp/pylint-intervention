from os import listdir
from os.path import join

import pandas as pd

BASE_DIR = 'c:/src/pylint-intervention'
DONE_DIRECTORY = join(BASE_DIR, "interventions/done/")

PR_COL = 'In which pull request the modification was done?'
HARMFUL_COL = 'Do you consider the removed alert harmful?'
NUM_HARMFUL_COL = 'Is harmful?'
BENEFIT_COL = 'What is the expected benefit(1 – negative, 5 – neutral, 10 – great)?'
REPO_COL = 'In which repository the modification was done?'

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
    g.to_csv(join(BASE_DIR
                    , 'interventions'
                    , 'all_done_interventions_stats.csv')
               , index=False)


if __name__ == "__main__":
    interventions_stats()
