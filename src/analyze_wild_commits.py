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


if __name__ == '__main__':
    analyze_wild_commits()
