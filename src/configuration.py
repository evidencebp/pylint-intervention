from os.path import join

BASE_DIR = 'c:/src/pylint-intervention/'
DONE_DIRECTORY = join(BASE_DIR, 'interventions/done/')
CANDIDATES_DIRECTORY = join(BASE_DIR, 'interventions/candidates/')
PROJECTS_DIR = 'c:/interventions/'

DATA_DIR = join(BASE_DIR, 'data/')
BEFORE_DIR = join(DATA_DIR, 'before/')
AFTER_DIR = join(DATA_DIR, 'after/')
DIFFS_DIR = join(DATA_DIR, 'diffs/')

METRICS_BEFORE_DIR = join(BASE_DIR
                          , "data/code_metrics/before/")
METRICS_AFTER_DIR = join(BASE_DIR
                         , "data/code_metrics/after/")


PR_COL = 'In which pull request the modification was done?'
HARMFUL_COL = 'Do you consider the removed alert harmful?'
HARMFUL_REASON_COL = 'Why do you consider it harmful (or harmless)?'
BENEFIT_COL = 'What is the expected benefit(1 – negative, 5 – neutral, 10 – great)?'
REPO_COL = 'In which repository the modification was done?'

EXCLUDED_REPOS = ['aajanki_yle-dl_interventions_October_06_2024.csv'  # For some reason computation takes too long
                  ]
