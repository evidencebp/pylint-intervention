# Pylint Intervention Experiment

## Summary

The use of static analysis alerts assumes that removing the cause of the alert improves the code. Justification mostly comes
from analysis of observations regarding their predictive power. These observations might be noisy due to interference of other
factors. Aim The goal of the experiment is to evaluate the benefit of fixing alerts of various types. Benefit will be measured by both developer opinion and in metric improvement.

## Experiment Status
Currently the experiment is in POC.
The goal of the POC is to fine tune the protocol and learn more about the interventions.
For example, how common are certain alerts and how long does it take to intervene and fix them.
Once the POC will be completed, the protocol will be finalized and we will move to large scale interventions.

## Method
We present the design of an intervention experiment on the Pylint static analyzer alerts. During the experiment we identify alerts in open-source projects and intervene to remove them.

## How to Contribute?

Unlike most open source projects, here you contribute by fixing alerts in other projects.

Please follow this procedure to contribute:

1. Verify that you have Python, Pylint and Pandas intalled
2. Pick a Java open source project.
3. Open an issue declaring the experiment, link to this paper and ask for approval to intervene. Continue only if the approval is given. If the community's developers are interested, they are welcome to participate too.
4. Fork the project, run it, run its tests and get familiar with it.
5. Download from the [tools](https://github.com/evidencebp/pylint-intervention/tree/main/tools) file and copy them into the project directory.
6. Run [run_pylint](https://github.com/evidencebp/pylint-intervention/blob/main/tools/run_pylint.py) to identify files with the relevant alerts.
7. run_pylint will generate a file called ``interventions.csv''.
8. Please go over the alerts by the order (to avoid bias) and intervene in the files to fix the alerts. You can fix as many alerts as you want.
9. However, please intervene only in files and alerts marked so, leaving the other as control.
10. Remove all occurrences of the alert and verify that by rerunning CheckStyle. Please make sure that your change is minimal. Avoid improving the file in other ways.
11. Run the tests, to verify that the change did not break the system.
12. Create a pull request (for all your interventions in the project).
13. In case that you are not part of the project community, please ask for a review by a non-community review first, to reduce their effort. We will be happy to be these reviewers if needed.
14. Submit the pull request and modify it by the feedback.
15. Fill the questions in ``interventions.csv'' with the pull request details (whether it was accepted or not).
16. Add the file at the [interventions directory](https://github.com/evidencebp/pylint-intervention/tree/main/interventions) in this project.

