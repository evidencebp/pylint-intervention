import os
from os.path import join
import re
import subprocess

import codecs

import pandas as pd

from configuration import PR_COL

def get_project_name(repo_name: str) -> str:

    return repo_name[repo_name.find("/")+1:]

def run_powershell_cmd(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)

    return completed

def delete_directory(dir: str):
    cmd = "Remove-Item -Recurse -Force {dir}".format(dir=dir)

    run_powershell_cmd(cmd)


def copy_files(source: str
               , target: str):
    cmd = "copy {source} {target}".format(source=source
                                          , target=target)

    run_powershell_cmd(cmd)


def move_files(source: str
               , target: str):
    cmd = "Move-Item -Path {source} -Destination {target}".format(source=source
                                          , target=target)

    run_powershell_cmd(cmd)



def clone_repo(repo_name: str
               , target_dir: str
               , recreate_if_exists: bool = False) -> bool:

    repo_dir = join(target_dir
                    , get_project_name(repo_name))
    already_exists = os.path.exists(repo_dir)
    if not already_exists or recreate_if_exists:
        cmd = "cd {dir};  git clone https://github.com/{repo_name}".format(dir=target_dir
                                                                   , repo_name=repo_name)
        run_powershell_cmd(cmd)

    return os.path.exists(repo_dir)



def pull_repo(repo_name: str
               , target_dir: str) -> bool:

    repo_dir = join(target_dir
                    , get_project_name(repo_name))
    cmd = "cd {dir};  git pull".format(dir=repo_dir)
    run_powershell_cmd(cmd)

    return os.path.exists(os.path.join(target_dir, get_project_name(repo_name)))

def count_repo_recent_commits(repo_dir: str
               , days: int) -> bool:

    cmd = "cd {dir};  git rev-list --count HEAD --since={days}.day".format(dir=repo_dir
                                                                   , days=days)
    result = run_powershell_cmd(cmd)

    so = result.stdout
    commits = int(str(so)[2:str(so).find("\\")]) # extracting from format "b'776\\n'"

    return commits



def get_file_prev_commit(commit, repo_dir):
    """ Find the commit in which a file was changed, prior to the current commit.
    """
    cmd = f"cd {repo_dir};   git log --format='format: %H'"
    result = run_powershell_cmd(cmd)

    commits = str(result.stdout)
    prev_commit_regex = commit + '\\\\n (?P<hash>[0-9a-f]{40})'
    match = re.search(prev_commit_regex, commits)

    return match.group('hash') if match else None

def show_file_content(file_name
                      , repo_dir
                      , commit=None
                      , output_file=None):
    """ Show file in a given commit version.
    """
    file_name = file_name.replace("\\", "/")
    if commit:
        command = f'cd {repo_dir}; git show %s:%s' % (commit, file_name)
    else:
        command = f'cd {repo_dir}; git show HEAD:%s' % file_name

    #result = str(run_powershell_cmd(command).stdout)[2:-1]
    result = run_powershell_cmd(command).stdout
    #result = str(result).encode("utf-8").replace("\n", os.linesep)
    result = str(result).replace(r"\n", os.linesep)[2:-1]
    if output_file:

        write_file(output_file, result)

    return result


def write_file(output_file
               , content
               , mode="w"):
    file = codecs.open(output_file
                       , mode
                       , "utf-8")
    file.write(content)
    file.close()


def get_branch_name(repo_dir: str) -> str:

    command = f'cd {repo_dir}; git branch --show-current'
    result = str(run_powershell_cmd(command).stdout)
    result = result[2:-1].replace(r"\n","")

    return result


def get_branch_names(repo_dir: str) -> str:

    command = f'cd {repo_dir}; git branch'
    result = str(run_powershell_cmd(command).stdout)
    result = result[2:-1].replace(r"\n","")

    return result

def create_branch(repo_dir: str
                  , branch_name: str
                  , commit: str = None):
    if commit:
        command = f'cd {repo_dir}; git branch {branch_name} {commit}'
    else:
        command = f'cd {repo_dir}; git branch {branch_name}'
    run_powershell_cmd(command)


def checkout_branch(repo_dir: str
                  , branch_name: str):

    command = f'cd {repo_dir}; git checkout {branch_name}'
    run_powershell_cmd(command)


def delete_branch(repo_dir: str
                    , branch_name: str):
    command = f'cd {repo_dir}; git branch -d {branch_name}'
    run_powershell_cmd(command)


def get_author_first_commit_in_repo(repo_dir: str
                                    , author_name: str = "evidencebp"):
    cmd = f"cd {repo_dir};   git log --author={author_name} --format='format: %H'"
    result = run_powershell_cmd(cmd)

    commit = str(result.stdout)
    commit = commit[commit.rfind("\\n") + 3:-1] # +3 due to "\\n ", -1 due to ending '

    return commit

def force_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def count_lines(file):
    with open(file, "rb") as f:
        num_lines = sum(1 for _ in f)

    return num_lines

def get_done_interventions(interventions_file):
    df = pd.read_csv(interventions_file)
    df = df[~df[PR_COL].isna()]
    df = df[df[PR_COL].str.contains('github')]

    return df


def encode_path(path
                , direction='both'):

    return path.replace("/", "_slash_").replace("\\", "_slash_")


def pylint_analysis(target: str
                    , config: str
                    , types : pd.DataFrame):
    ALERTS_FILE = "alerts.csv"

    # get alerts
    PYLINT_CMD = f"pylint --rcfile={config} --score=n" \
                 + " --msg-template='{path},{line},{msg_id}' " + f"{target} > " \
                 + ALERTS_FILE
    os.system(PYLINT_CMD)
    lines = count_lines(ALERTS_FILE)
    if lines:
        df = pd.read_csv(ALERTS_FILE, skiprows=1, header=None)

        # aggregate alerts
        df.columns = ['path', 'line', 'msg_id']
        df = pd.merge(df
                      , types
                      , on='msg_id'
                      , how='left')

        df = df[df['path'].notna()
                & df['line'].notna()
                & df['msg_id'].notna()
                & df['msg'].notna()]  # Filter out bad parsing
        agg = df.groupby(['path', 'msg_id']
                         , as_index=False).agg({'line': 'count'
                                                   , 'msg': 'max'})  # Message is similar
        # , max chooses one
        agg.rename(columns={'line': 'alerts'}
                   , inplace=True)
    else:
        os.remove(ALERTS_FILE)
        agg = None

    return agg


def get_all_commits(repo_dir: str
                    , git_format="'format: %H %aE %cD'"
                    , format_regex='(?P<hash>[0-9a-f]{5,40}) (?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+) (?P<time>.{25})'
                    , columns=['commit', 'email', 'commit_time']
                    , since=None
                    , until=None
                    , target=None):
    """ Returns all the commits in a given period of time.
        The parameters git_format, format_regex and columns are given to
        allow flexibility.
        git format should provided the information that will be parsed
        using format_regex and stored in the data frame columns
    """
    # Date format is '1 Nov 2016'
    command = f"cd {repo_dir} ; "
    command = command + "git log --format=%s" % git_format
    command = command + (" --since='%s' " % since) if since else command
    command = command + (" --until='%s' " % until) if until else command
    command = command + (" " + target) if target else command

    commits = run_powershell_cmd(command)
    commits = str(commits.stdout)
    commits = str(commits)[3:-1]
    matches = re.findall(format_regex, commits)

    return pd.DataFrame(matches
                        , columns=columns)

def copy_file_at_commit(repo_dir: str
                        , source_file: str
                        , target_path: str
                        , commit: str):
    # Get current branch
    intervention_branch = get_branch_name(repo_dir=repo_dir)
    pre_branch_name = 'tmp_branch'

    # Move to pre-intervention branch
    create_branch(repo_dir=repo_dir
                  , branch_name=pre_branch_name
                  , commit=commit)
    checkout_branch(repo_dir=repo_dir
                    , branch_name=pre_branch_name)


    copy_files(source=join(repo_dir
                                          , source_file)
                    , target=target_path)

    # Return to original branch
    checkout_branch(repo_dir=repo_dir
                    , branch_name=intervention_branch)
    # Delete temp branch
    delete_branch(repo_dir=repo_dir
                  , branch_name=pre_branch_name)


