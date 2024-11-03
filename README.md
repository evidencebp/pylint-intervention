# [Pylint](https://pypi.org/project/pylint/) Intervention Experiment

## Summary

The use of static analysis alerts assumes that removing the cause of the alert improves the code. Justification mostly comes
from analysis of observations regarding their predictive power. These observations might be noisy due to interference of other
factors. Aim The goal of the experiment is to evaluate the benefit of fixing alerts of various types. Benefit will be measured by both developer opinion and in metric improvement.

See examples of interventions in [stanford-oval/storm](https://github.com/stanford-oval/storm/pull/181), [gabfl/vault](https://github.com/gabfl/vault/pull/82), and [coreruleset/coreruleset](https://github.com/coreruleset/coreruleset/pull/3837).


## What's in it for Me?
Participating in the project is an opportunity to contribute to both science and open source.We will acknowledge all contributions. More than that, we would like to publish an academic paper based on the experiment in a [research turk](https://arxiv.org/pdf/2001.01972) like method. Contributors that will do 50 interventions and match the publisher conditions (e.g., approval of paper, responsibility to content) will be authors of the paper.

## Experiment Status
Currently the experiment is in POC.
The goal of the POC is to fine tune the protocol and learn more about the interventions.
For example, how common are certain alerts and how long does it take to intervene and fix them.
Once the POC will be completed, the protocol will be finalized and we will move to large scale interventions.

## Method
We present the design of an intervention experiment on the Pylint static analyzer alerts. During the experiment we identify alerts in open-source projects and intervene to remove them.

## How to Contribute?

Unlike most open source projects, here you contribute by fixing alerts in other projects.
Therefore, start in [commenting that you would like to contribute](https://github.com/evidencebp/pylint-intervention/issues/1), and if you have a suitable project, please [recommend](https://github.com/evidencebp/pylint-intervention/issues/2).

Please follow this procedure to contribute:

1. Verify that you have Python, Pylint and Pandas intalled
2. Pick a Python open source project. The [candidates](https://github.com/evidencebp/pylint-intervention/tree/main/interventions/candidates) directory has projects with their alerts statistics.
3. Check in the [repositories file](https://github.com/evidencebp/pylint-intervention/blob/main/interventions/repositories.csv) the repository status.
4. If the repository is not there, continue. If the intervention was rejected, please choose a different repository. If there was an intervention, you can still intervene yet in different files.
5. Read the contribution guidelines. That should help to see that the experiment does not contradict them. Please follow the guideline during the process.
6. Open an issue declaring the experiment, link to this paper and ask for approval to intervene. Continue only if the approval is given. If the community's developers are interested, they are welcome to participate too.
7. Fork the project, run it, run its tests and get familiar with it.
8. Download from the [tools](https://github.com/evidencebp/pylint-intervention/tree/main/tools/project_analysis) file and copy them into the project directory.
9. Run [run_pylint](https://github.com/evidencebp/pylint-intervention/blob/main/tools/project_analysis/run_pylint.py) to identify files with the relevant alerts.
10. run_pylint will generate a file called ``interventions.csv''.
11. Please go over the alerts by the order (to avoid bias) and intervene in the files to fix the alerts. You can fix as many alerts as you want.
12. However, please intervene only in files and alerts marked so, leaving the other as control.
13. Remove all occurrences of the alert and verify that by rerunning Pylint. Please make sure that your change is minimal. Avoid improving the file in other ways.
14. Run the tests, to verify that the change did not break the system.
15. Create a pull request (for all your interventions in the project).
16. In case that you are not part of the project community, please ask for a review by a non-community review first, to reduce their effort. We will be happy to be these reviewers if needed.
17. Submit the pull request and modify it by the feedback.
18. Fill the questions in ``interventions.csv'' with the pull request details (whether it was accepted or not).
19. Add the file at the [done interventions directory](https://github.com/evidencebp/pylint-intervention/tree/main/interventions/done) in this project.

## Choice of Alerts

In principle, the experiment can be conducted with any alerts, and evaluate their contributions.Since we need to perform enough interventions per alert we do not work on all of them but focus on a smaller group.
We avoid alerts that identify a syntax error or a clear bug (e.g., "duplicate-argument-name (E0108)") since we are interested in code quality in general.We prefer alerts for which there is prior research regarding their benefit (e.g., "too-many-branches (R0912)").Note that all alerts in Pylint are considered beneficial enough to implement and maintain.Therefore we think that the project will benefit from the internations.
There are alerts in which the computer is indifferent yet there might be indirect influence via the developer.For example, "unnecessary-pass (W0107)" is probably a leftover and not an intended implementation.We include such alert since it it known that removing them might be beneficial (e.g., see [the benefits of dead code removal](https://www.cs.huji.ac.il/w~feit/papers/Refactor19PROMISE.pdf)) .A direct local removal of such alerts will allow to differ their influence and the influence of removing them in a general cleanup.

We do not specify how to intervene and fix the alert, similar to alerts encountered in regular software development.
However, the alerts usually specify a clear problem like "line-too-long (C0301)".
The developer should make the line shorter.
However, this can be done by simply adding a line break or by introducing an auxiliary variable, emphasizing a semantic meaning.

## Choice of files
We exclude test files since they might behave differently from functional files.We require 5 commits in the last 90 days in order to enable the usage of process metrics (e.g., [tendency to bugs, commit duration](https://link.springer.com/article/10.1007/s11219-021-09564-z)).
We split the files into two groups, in one we can intervene and the other is left as is for comparison.In the internevne group we select a single alert , which does not appear too much as the one to fix.This is done in order to keep the intervention small and specific.
