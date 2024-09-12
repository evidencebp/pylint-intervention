import os

import pandas as pd

# TODO - handle subdriectories
ALERTS_FILE = "alerts.txt"
AGG_ALERTS_FILE = "agg_alerts.txt"

# get alerts
PYLINT_CMD = "pylint  --rcfile=pylint_short.cfg --score=n --msg-template='{path},{line},{msg_id}' . >  " + ALERTS_FILE
alerts = os.system(PYLINT_CMD)
df = pd.read_csv(ALERTS_FILE, skiprows=1, header=None)

# aggregate alerts
df.columns = ['path', 'line', 'msg_id']
agg = df.groupby(['path', 'msg_id']
                 , as_index=False).agg({'line': 'count'})
agg.rename(columns={'line': 'alerts'}
           , inplace=True)
agg.to_csv(AGG_ALERTS_FILE
           , index=False)