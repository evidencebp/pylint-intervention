from os import listdir
from os.path import join

import pandas as pd

from configuration import DONE_DIRECTORY

def clean_whitespace():
    intervention_files = listdir(DONE_DIRECTORY)

    for i in intervention_files:
        df = pd.read_csv(join(DONE_DIRECTORY
                              , i))
        df['msg'] = df['msg'].map(lambda x: x.strip())
        df.to_csv(join(DONE_DIRECTORY
                              , i)
                  , index=False)

if __name__ == "__main__":
    clean_whitespace()
