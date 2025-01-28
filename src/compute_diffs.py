import datetime
from os import listdir

from os.path import join
import pandas as pd

from configuration import (DONE_DIRECTORY, REPO_COL, BASE_DIR
                                , BEFORE_DIR, AFTER_DIR,DIFFS_DIR, EXCLUDED_REPOS, PROJECTS_DIR)
from utils import (get_author_first_commit_in_repo, get_project_name, get_file_prev_commit
                    , get_branch_name, create_branch, checkout_branch, delete_branch
                    , force_dir, copy_files, get_done_interventions, count_lines)


def copy_repo_files(target_directory: str
                    , repo_name:str
                    , interventions_df:pd.DataFrame):

    # Create repo dir if needed
    repo_dir = join(target_directory
                    , get_project_name(repo_name))

    force_dir(repo_dir)

    for i in interventions_df['path'].unique():
        source = join(PROJECTS_DIR
                      , get_project_name(repo_name)
                      , i)
        dest = join(target_directory
                    , get_project_name(repo_name)
                    , i.replace("\\", "_slash_"))
        copy_files(source
                   , dest)

def build_repo_varsion(interventions_file
                         , current=True):
    df = get_done_interventions(interventions_file)

    repo_name = df[REPO_COL].astype(str).max()  # Should be same value, max takes one
    repo_dir = join(PROJECTS_DIR
                    , get_project_name(repo_name))

    if not current:
        first_intervention_commit = get_author_first_commit_in_repo(repo_dir=repo_dir)
        pre_intervention_commit = get_file_prev_commit(commit=first_intervention_commit
                                                       , repo_dir=repo_dir)
        # Get current branch
        intervention_branch = get_branch_name(repo_dir=repo_dir)
        pre_branch_name = 'tmp_branch'

        # Move to pre-intervention branch
        create_branch(repo_dir=repo_dir
                      , branch_name='tmp_branch'
                      , commit=pre_intervention_commit)
        checkout_branch(repo_dir=repo_dir
                        , branch_name=pre_branch_name)


    if current:
        copy_repo_files(target_directory=join(BASE_DIR
                                              , 'data/after')
                        , repo_name=repo_name
                        , interventions_df=df)

    else:
        copy_repo_files(target_directory=join(BASE_DIR
                                              , 'data/before')
                        , repo_name=repo_name
                        , interventions_df=df)

        # Return to original branch
        checkout_branch(repo_dir=repo_dir
                        , branch_name=intervention_branch)
        # Delete temp branch
        delete_branch(repo_dir=repo_dir
                      , branch_name=pre_branch_name)


def build_all_repo_versions():

    intervention_files = listdir(DONE_DIRECTORY)
    intervention_files = set(intervention_files) - set(EXCLUDED_REPOS)


    for i in intervention_files:
        print(datetime.datetime.now(), i)
        for c in [True, False]:
            build_repo_varsion(interventions_file=join(DONE_DIRECTORY
                              , i)
                               , current=c)

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
    build_all_repo_versions()
    # compute_versions_diff()
    #compute_diff_sizes()


