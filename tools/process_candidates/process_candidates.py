import os
import subprocess
import datetime


import pandas as pd

CLONE_DIR = "c:/src/"
ANALYSIS_DIR = "C:/src/pylint-intervention/tools/project_analysis/"
INTERNATIONS_DIR = "C:/src/pylint-intervention/interventions/"

# Duplicated deliberately from run_pylint, to keep not related
AGG_ALERTS_FILE = "interventions.csv"

def process_candidates(candidates_file: pd.DataFrame
                       , stats_file: str
                       , delete_no_alerts: bool = False):

    df = pd.read_csv(candidates_file)

    print(len(df), "repos to process")
    cur_num = 1
    all_stats = []

    for _, i in df.iterrows():
        print("{time} processing repo #{num} {name}".format(time=datetime.datetime.now()
                                                                , num=cur_num
                                                                ,name=i['repo_name']))
        cur_num = cur_num + 1
        
        stats = process_cancidate(repo_name=i['repo_name']
                                  , delete_no_alerts=delete_no_alerts)
        all_stats.append(stats)

    stats_df = pd.concat(all_stats)
    stats_df.to_csv(stats_file
                    , index=False)

def process_cancidate(repo_name: str
                      , delete_no_alerts: bool = False) -> pd.DataFrame:

    try:
        cloned = clone_repo(repo_name)

        if cloned:
            # Analyze results

            # Delete repo without alerts
            has_alerts = analyze_repo(repo_name)
            if has_alerts:
                df = get_interventions_stats(repo_name)
                today = datetime.date.today()

                copy_files(source=os.path.join(CLONE_DIR
                                        , get_project_name(repo_name)
                                        , AGG_ALERTS_FILE)
                           , target=os.path.join(INTERNATIONS_DIR
                                                 , "{repo}_interventions_{date}.csv".format(
                                                    repo=repo_name.replace("/", "_")
                                                    , date=today.strftime("%B_%d_%Y"))))

            else:
                if delete_no_alerts:
                    delete_directory(os.path.join(CLONE_DIR, get_project_name(repo_name)))

                df = pd.DataFrame([(repo_name, 'no alerts', datetime.datetime.now(), 0, 0, 0, None)]
                                  , columns=['repo_name', 'status', 'time'
                        , 'alerts', 'interventions', 'intervention_types', 'comment'])
        else:
            df = pd.DataFrame([(repo_name, 'not cloned', datetime.datetime.now(), 0, 0,0, None)]
                            , columns=['repo_name', 'status', 'time'
                                        , 'alerts', 'interventions', 'intervention_types', 'comment'])
    except Exception:
        df = pd.DataFrame([(repo_name, 'exception', datetime.datetime.now(), 0, 0, 0, None)]
                          , columns=['repo_name', 'status', 'time'
                , 'alerts', 'interventions', 'intervention_types', 'comment'])

    return df

def clone_repo(repo_name: str) -> bool:

    cmd = "cd {dir};  git clone https://github.com/{repo_name}".format(dir=CLONE_DIR
                                                                   , repo_name=repo_name)
    run_powershell_cmd(cmd)

    return os.path.exists(os.path.join(CLONE_DIR, get_project_name(repo_name)))

def analyze_repo(repo_name) -> bool:

    project_path = os.path.join(CLONE_DIR
                           , get_project_name(repo_name))
    # copy tool
    cmd = "copy {tool}/* {project_path}".format(tool=ANALYSIS_DIR
                                                       , clone_dir=CLONE_DIR
                                                       , project_path=project_path)
    run_powershell_cmd(cmd)

    cmd = "cd {project_path}; python run_pylint.py".format(project_path=project_path)
    run_powershell_cmd(cmd)

    return os.path.exists(os.path.join(CLONE_DIR
                           , get_project_name(repo_name)
                            , 'alerts.csv'))

def get_interventions_stats(repo_name: str) -> pd.DataFrame:
    df = pd.read_csv(os.path.join(CLONE_DIR
                           , get_project_name(repo_name)
                            , AGG_ALERTS_FILE))


    stats = pd.DataFrame([(repo_name
                           , 'alerts'
                           , datetime.datetime.now()
                           , len(df)
                           , len(df[df['chosen'] ==1])
                           , df[df['chosen'] ==1]['msg_id'].nunique()
                           , None)]
                  , columns=['repo_name', 'status', 'time', 'alerts', 'interventions', 'intervention_types', 'comment'])

    return stats


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


def compute_stats(candidates_file: pd.DataFrame
                       , stats_file: str):
    df = pd.read_csv(candidates_file)


    print(len(df), "repos to process")
    cur_num = 1
    all_stats = []

    for _, i in df.iterrows():
        print("{time} processing repo #{num} {name}".format(time=datetime.datetime.now()
                                                            , num=cur_num
                                                            , name=i['repo_name']))
        cur_num = cur_num + 1

        repo_name = i['repo_name']
        if os.path.exists(os.path.join(CLONE_DIR
                           , get_project_name(repo_name)
                            , AGG_ALERTS_FILE)):
            stats = get_interventions_stats(repo_name)

            all_stats.append(stats)

    stats_df = pd.concat(all_stats)
    stats_df.to_csv(stats_file
                    , index=False)


if __name__ == "__main__":

    candidates_file = "C:\src\pylint-intervention\candidate_repos\python_repos_above_50_by_2023_properties_year22.csv"
    stats_file = "c:/tmp/new_stats.csv"
    #process_cancidate(repo_name="niklasf/python-chess"
    #                    , delete_no_alerts=True)
    process_candidates(candidates_file=candidates_file
                            , stats_file=stats_file
                            , delete_no_alerts=False)

    #get_interventions_stats("GafferHQ/gaffer")
    #compute_stats(candidates_file=candidates_file
    #                        , stats_file="c:/tmp/python_repos_above_50_by_2023_properties_year22_interventions_v2.csv")
