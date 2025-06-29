from os.path import join
import pandas as pd

LABELS_DIR = "C:/src/comp/data"

labels_files = {'added_functions_hits': ["is_refactor_label",	"is_clean_label", "added_functions_label"]
                , "reduced_McCabe_max_hits": ["is_refactor_label",	"is_clean_label", "reduced_McCabe_max_label"]
                , "suitable_reduced_McCabe_max_hits": ["is_refactor_label",	"is_clean_label"#, "added_functions"
                                                       , "reduced_McCabe_max_label", "mostly_delete", "massive_change"]}

def evaluate_performance():

    for file in labels_files.keys():
        df = pd.read_csv(join(LABELS_DIR
                              , file + '.csv'))
        df = df[~df["is_refactor_label"].isna()]
        print(file, "records: ", len(df))

        for i in labels_files[file]:
            print(" "*5, i, "hit rate", df[i].mean())
            print(" "*5, i, "precision predicting refactor rate", df[df[i]==True].is_refactor_label.mean())


def check_duplications():
    dfs = []
    for file in labels_files.keys():
        df = pd.read_csv(join(LABELS_DIR
                              , file + '.csv'))
        df = df[~df["is_refactor_label"].isna()]
        df = df[["commit",	"file_name_x", "alert"]]
        df['location'] = file
        dfs.append(df)

    commits_df = pd.concat(dfs)
    g = commits_df.groupby(["commit","file_name_x"]
                           , as_index=False).agg({'alert': 'count'
                                                  , 'location': lambda x: ', '.join(x)})
    g = g[g["alert"]>1]
    print(g)


if __name__ == "__main__":
    evaluate_performance()
    check_duplications()

