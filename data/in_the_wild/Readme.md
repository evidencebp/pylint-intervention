Even if we build a dataset with many interventions, most of the interventions performed in open source projects will not be in the dataset.
However, our dataset will allow us to find and validate [labeling functions](https://dl.acm.org/doi/10.1145/3661167.3661224).
Labeling functions are weak classifiers , models whose performance need to be only slightly better than a guess.
Labeling functions are common in weakly-supervised learning  , where one is required to do supervised-learning yet lacks labels.
Their predictions compensate for the lacking labels.

Consider the "extract method" which is called the “Swiss army knife” of refactoring.
Possible labeling functions for it are reference to method extraction in commit message, reduction in the maximal McCabe complexity, and of course introduction of new functions and calling them from the modified function.
We can build such labeling functions and evaluate their predictive performance (e.g., recall) using our dataset.
Once we have the labeling functions, we can run them on open source projects and identify interventions in vivo.
That will allow us to evaluate the impact of the interventions on the containing file and project.
That scale will allow robust analysis on a variety of cases.
That will be valuable also for alerts of semantic nature (e.g., wildcard-import and broad-exception-caught) whose change is not captured in only code metrics.

So, we take here [two versions of the same file](https://arxiv.org/pdf/2112.11858) in two dates, 6 months apart.
We run Pylint and look for alerts that were removed.
6 month is a long period, so we would like to use the labeling functions to identify the removal commit.
If the removal is clean, we can use it as an intervention.
