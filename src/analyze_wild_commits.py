import pandas as pd

from compute_commit_profile import ENHANCED_FILE, PROFILES_FILE

def analyze_wild_commits():
    df = pd.read_csv(ENHANCED_FILE)

    print('Cases per alert state')
    print(df.state.value_counts().sort_index())

    df = df[df['state']=='removed']

    variables = ['is_refactor', 'only_removal', 'mostly_delete', 'massive_change', 'is_clean']

    for i in variables:
        print(i)
        print(df[i].value_counts(normalize=True))

    print("Massive change and clean by alert")
    print(df.groupby(['alert']
            , as_index=False).agg({'commit': 'count'
                                    , 'massive_change': 'mean'
                                    , 'is_clean': 'mean'}))


def analyze_ccp_groups():
    df = pd.read_csv(ENHANCED_FILE)


    df = df[df['state']=='removed']
    df['ccp_group'] = df['ccp_pm_before'].map(lambda x: 'low' if x < 0.09 else 'high' if x > 0.39 else 'med')

    print("Change by CCP group")
    print(df[(df.state.isin(['removed', 'decrease']))
             & (df['mostly_delete'] == False)
             & (df['massive_change'] == False)
             ].groupby(['ccp_group']
                , as_index=False).agg({'commit': 'count'
                                        , 'ccp_diff': 'mean'
                                        , 'same_day_duration_avg_diff': 'mean'}))

    print("Change by CCP group and alert")
    print(df[(df.state.isin(['removed', 'decrease']))
             & (df['mostly_delete'] == False)
             & (df['massive_change'] == False)
             ].groupby(['alert', 'ccp_group']
             , as_index=False).agg({'commit': 'count'
                                    , 'ccp_diff': 'mean'
                                    ,  'same_day_duration_avg_diff': 'mean'}))

if __name__ == '__main__':
    analyze_wild_commits()
