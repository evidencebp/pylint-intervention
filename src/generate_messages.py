from os.path import join

import pandas as pd
import pprint

from configuration import CANDIDATES_DIRECTORY, HARMFUL_COL, HARMFUL_REASON_COL

readability_alerts = ['superfluous-parens'
    , 'try-except-raise'
    , 'unnecessary-semicolon'
    , 'line-too-long'
    , 'wildcard-import'
                      ]
possible_bug_alerts = ['unnecessary-pass'
    , 'pointless-statement'
    , 'using-constant-test'
    , 'comparison-of-constants'
    , 'broad-exception-caught'
                       ]

simplification_alerts = ['simplifiable-if-statement'
    , 'Simplify-boolean-expression'
    , 'simplifiable-if-expression'
    , 'simplifiable-condition'
    , 'too-many-boolean-expressions']
structure_alerts = ['too-many-lines'
    , 'duplicate-code'
    , 'too-many-return-statements'
    , 'too-many-branches'
    , 'too-many-statements'
    , 'too-many-nested-blocks'
                    ]


def generate_intro(interventions_file):
    template = """Pylint alerts are correlated with tendency to bugs and harder maintenance.
I'd like to conduct a software engineering experiment regarding the benefit of [Pylint](https://pypi.org/project/pylint/) alerts removal.
The experiment is described [here](https://github.com/evidencebp/pylint-intervention/).

In the experiments, Pylint is used with some specific alerts, files are selected for intervention and control.
After the interventions are done, one can wait and examine the results.

Your repository is expected to benefit from the interventions.
I'm asking for your approval for conducting an intervention in your repository.

See examples of interventions in [stanford-oval/storm](https://github.com/stanford-oval/storm/pull/181), [gabfl/vault](https://github.com/gabfl/vault/pull/82), and [coreruleset/coreruleset](https://github.com/coreruleset/coreruleset/pull/3837).

You can see the [planed interventions](https://github.com/evidencebp/pylint-intervention/tree/main/interventions/candidates/{interventions_file})

May I do the interventions?"""

    print("Pylint alerts corrections as part of an intervention experiment")
    print("#"*50)
    print(template.format(interventions_file=interventions_file))
    print()
    print()
    print("#"*50)



def generate_pr_creation(issue_url):
    template = """Makes the interventions describe in [intervention issue]({issue_url}).
The experiment is described [here](https://github.com/evidencebp/pylint-intervention/).

Each intervention was done in a dedicated commit with a message explaining it.
"""

    print("Pylint alerts corrections as part of an intervention experiment"
          , issue_url[issue_url.rfind("/") + 1:])
    print("#" * 50)
    print(template.format(issue_url=issue_url))


def get_plan_metrics(interventions_file):
    path = join(CANDIDATES_DIRECTORY
                , interventions_file)
    df = pd.read_csv(path)
    df = df[df.chosen==1]
    df['msg'] = df['msg'].map(lambda x: x.strip())


    stats = {'file':  len(df)
             , 'interventions_number': df['alerts'].sum()
             , 'interventions_types_number': df['msg'].nunique()
             , 'readability_alerts': df[df['msg'].isin(readability_alerts)]['alerts'].sum()
             , 'possible_bug_alerts': df[df['msg'].isin(possible_bug_alerts)]['alerts'].sum()
             , 'simplification_alerts': df[df['msg'].isin(simplification_alerts)]['alerts'].sum()
             , 'structure_alerts': df[df['msg'].isin(structure_alerts)]['alerts'].sum()
             , 'interventions_types': list(df['msg'].unique())
             }

    for alert in df['msg'].unique():
        stats[alert] = df[df['msg'] == alert]['alerts'].sum()

    return stats


def get_plan_discussion(interventions_file):
    path = join(CANDIDATES_DIRECTORY
                , interventions_file)
    df = pd.read_csv(path)
    df = df[df.chosen==1]
    print(df[HARMFUL_COL].value_counts()) # To see that there are no spelling problems
    df = df[df[HARMFUL_COL]=='Discuss']
    df['msg'] = df['msg'].map(lambda x: x.strip())

    df = df.sort_values('msg')
    #print(df[['msg', 'path', HARMFUL_REASON_COL]])
    for _, i in df[['msg', 'path', HARMFUL_REASON_COL]].iterrows():
        print(i['msg'])
        print(i['path'])
        print(i[HARMFUL_REASON_COL])

if __name__ == "__main__":

    pp = pprint.PrettyPrinter(depth=4)
    #pp.pprint(mydict)

    interventions_file = "materialsproject_MPContribs_interventions_October_06_2024.csv"
    #generate_intro(interventions_file)
    #pp.pprint(get_plan_metrics(interventions_file))
    #generate_pr_creation("https://github.com/materialsproject/MPContribs/issues/1853")
    get_plan_discussion(interventions_file)
