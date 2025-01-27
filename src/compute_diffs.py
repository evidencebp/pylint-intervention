from os import listdir

from os.path import join
import pandas as pd

from configuration import (DONE_DIRECTORY, REPO_COL
                                , BEFORE_DIR, AFTER_DIR,DIFFS_DIR)
from utils import (get_project_name, force_dir, count_lines)

from compute_code_metrics import EXCLUDED_REPOS, get_done_interventions

def compute_versions_diff():
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    diff_file = open("c:/tmp/diff.ps1", "w")
    for i in intervention_files:
        df = get_done_interventions(join(DONE_DIRECTORY
                                         , i))
        repo_name = df[REPO_COL].astype(str).max()  # Should be same value, max takes one

        for f in df['path'].unique():
            fname = f.replace("\\", "_slash_")

            target_dir = join(DIFFS_DIR
                           , get_project_name(repo_name))
            force_dir(target_dir)
            first = join(BEFORE_DIR
                         , get_project_name(repo_name)
                         , fname)
            second = join(AFTER_DIR
                            , get_project_name(repo_name)
                            , fname)
            target = join(DIFFS_DIR
                            , get_project_name(repo_name)
                            , fname.replace(".py", ".txt"))
            """
            git_diff(first=join(BEFORE_DIR
                                , get_project_name(repo_name)
                                , fname)
                        , second=join(AFTER_DIR
                                            , get_project_name(repo_name)
                                            , fname)
                        , target=join(DIFFS_DIR
                                       , get_project_name(repo_name)
                                       , fname.replace(".py", ".txt")))
            """
            cmd = f" git diff {first} {second} "
            if target:
                cmd = cmd + f" > {target} "
            #print(cmd)
            diff_file.write(cmd)
            diff_file.write("\n\n")

    diff_file.close()


def compute_diff_sizes():
    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)

    sizes = []
    for i in intervention_files:
        df = get_done_interventions(join(DONE_DIRECTORY
                                         , i))
        repo_name = df[REPO_COL].astype(str).max()  # Should be same value, max takes one

        for f in df['path'].unique():
            fname = f.replace("\\", "_slash_")

            target = join(DIFFS_DIR
                            , get_project_name(repo_name)
                            , fname.replace(".py", ".txt"))
            size = count_lines(target)
            sizes.append((repo_name, f, size))

    df = pd.DataFrame(sizes
                      , columns=['repo_name', 'file', 'size'])
    df.to_csv(join(DIFFS_DIR
                   , 'diff_sizes.csv')
              , index=False)

if __name__ == "__main__":
    # compute_versions_diff()
    compute_diff_sizes()


