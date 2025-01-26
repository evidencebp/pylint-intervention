from os import listdir
from os.path import join

import pandas as pd

from configuration import DONE_DIRECTORY, REPO_COL

def clean_whitespace(field):
    intervention_files = listdir(DONE_DIRECTORY)

    for i in intervention_files:
        df = pd.read_csv(join(DONE_DIRECTORY
                              , i))
        df[field] = df[field].map(lambda x: str(x).strip())
        df.to_csv(join(DONE_DIRECTORY
                              , i)
                  , index=False)

if __name__ == "__main__":
    #clean_whitespace(field='msg')
    clean_whitespace(field=REPO_COL)

