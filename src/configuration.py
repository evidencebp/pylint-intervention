from os.path import join

BASE_DIR = 'c:/src/pylint-intervention/'
DONE_DIRECTORY = join(BASE_DIR, 'interventions/done/')
CANDIDATES_DIRECTORY = join(BASE_DIR, 'interventions/candidates/')
PROJECTS_DIR = 'c:/interventions/'

PR_COL = 'In which pull request the modification was done?'
HARMFUL_COL = 'Do you consider the removed alert harmful?'
HARMFUL_REASON_COL = 'Why do you consider it harmful (or harmless)?'
BENEFIT_COL = 'What is the expected benefit(1 – negative, 5 – neutral, 10 – great)?'
REPO_COL = 'In which repository the modification was done?'
