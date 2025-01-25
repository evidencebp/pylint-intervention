import os
from os.path import join
import re
import subprocess

import codecs


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
               , target_dir: str) -> bool:

    cmd = "cd {dir};  git clone https://github.com/{repo_name}".format(dir=target_dir
                                                                   , repo_name=repo_name)
    run_powershell_cmd(cmd)

    return os.path.exists(os.path.join(target_dir, get_project_name(repo_name)))



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

        file = codecs.open(output_file, "w", "utf-8")
        file.write(result)
        file.close()

    return result

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
