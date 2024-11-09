import os
from os.path import join
import subprocess


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

