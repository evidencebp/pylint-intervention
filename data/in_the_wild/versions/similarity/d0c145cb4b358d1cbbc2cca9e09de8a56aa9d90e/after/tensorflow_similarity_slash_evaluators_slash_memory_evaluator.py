from collections import defaultdict
from copy import copy
import math
from typing import DefaultDict, Dict, List, Mapping, Sequence, Union

import tensorflow as tf
from tqdm.auto import tqdm

from .evaluator import Evaluator
from tensorflow_similarity.classification_metrics import ClassificationMetric
from tensorflow_similarity.matchers import ClassificationMatch
from tensorflow_similarity.matchers import make_classification_matcher
from tensorflow_similarity.retrieval_metrics import make_retrieval_metric
from tensorflow_similarity.retrieval_metrics import RetrievalMetric
from tensorflow_similarity.retrieval_metrics.utils import compute_match_mask
from tensorflow_similarity.types import (
        Lookup, CalibrationResults, IntTensor, FloatTensor)
from tensorflow_similarity.utils import unpack_lookup_distances
from tensorflow_similarity.utils import unpack_lookup_labels


class MemoryEvaluator(Evaluator):
    """In memory index performance evaluation and classification."""

    def evaluate_retrieval(
            self,
            *,
            target_labels: Sequence[int],
            lookups: Sequence[Sequence[Lookup]],
            retrieval_metrics: Sequence[Union[str, RetrievalMetric]],
            distance_rounding: int = 8) -> Dict[str, Union[float, int]]:
        """Evaluates lookup performances against a supplied set of metrics

        Args:
            target_labels: Sequence of the expected labels to match.

            lookups: Sequence of lookup results as produced by the
            `Index().batch_lookup()` method.

            retrieval_metrics: Sequence of `RetrievalMetric()` to evaluate
            lookup matches against.

            distance_rounding: How many digit to consider to decide if
            the distance changed. Defaults to 8.

        Returns:
            Dictionary of metric results where keys are the metric names and
            values are the metrics values.
        """
        # [nn[{'distance': xxx}, ]]
        # normalize metrics
        eval_metrics: List[RetrievalMetric] = (
            [make_retrieval_metric(m) for m in retrieval_metrics])

        # data preparation: flatten and rounding
        # lookups will be shape(num_queries, num_neighbors)
        # distances will be len(num_queries x num_neighbors)
        nn_labels = unpack_lookup_labels(lookups)
        distances = unpack_lookup_distances(lookups, distance_rounding)
        # ensure the target labels are an int32 tensor
        target_labels = tf.convert_to_tensor(target_labels, dtype='int32')
        match_mask = compute_match_mask(target_labels, nn_labels)

        # compute metrics
        evaluation = {}
        for m in eval_metrics:
            evaluation[m.name] = m.compute(
                query_labels=target_labels,
                lookup_labels=nn_labels,
                lookup_distancess=distances,
                match_mask=match_mask
            )

        return evaluation

    def evaluate_classification(
        self,
        *,
        query_labels: IntTensor,
        lookup_labels: IntTensor,
        lookup_distances: FloatTensor,
        distance_thresholds: FloatTensor,
        metrics: Sequence[ClassificationMetric],
        matcher: Union[str, ClassificationMatch],
        distance_rounding: int = 8,
        verbose: int = 1
    ) -> Dict[str, Union[float, int]]:
        """Evaluate the classification performance.

        Compute the classification metrics given a set of queries, lookups, and
        distance thresholds.

        Args:
            query_labels: Sequence of expected labels for the lookups.

            lookup_labels: A 2D tensor where the jth row is the labels
            associated with the set of k neighbors for the jth query.

            lookup_distances: A 2D tensor where the jth row is the distances
            between the jth query and the set of k neighbors.

            distance_thresholds: A 1D tensor denoting the distances points at
            which we compute the metrics.

            metrics: The set of classification metrics.

            matcher: {'match_nearest', 'match_majority_vote'} or
            ClassificationMatch object. Defines the classification matching,
            e.g., match_nearest will count a True Positive if the query_label
            is equal to the label of the nearest neighbor and the distance is
            less than or equal to the distance threshold.

            distance_rounding: How many digit to consider to
            decide if the distance changed. Defaults to 8.

            verbose: Be verbose. Defaults to 1.
        Returns:
            A Mapping from metric name to the list of values computed for each
            distance threshold.
        """
        matcher = make_classification_matcher(matcher)
        matcher.compile(distance_thresholds=distance_thresholds)

        # compute the tp, fp, tn, fn counts
        matcher.match(
                query_labels=query_labels,
                lookup_labels=lookup_labels,
                lookup_distances=lookup_distances)

        # evaluating performance as distance value increase
        if verbose:
            pb = tqdm(total=len(metrics), desc='Evaluating')

        # evaluating performance as distance value increase
        results = {'distance': distance_thresholds}
        for m in metrics:
            res = m.compute(
                    tp=matcher.tp,
                    fp=matcher.fp,
                    tn=matcher.tn,
                    fn=matcher.fn,
                    count=matcher.count)
            results[m.name] = res

            if verbose:
                pb.update()

        if verbose:
            pb.close()

        return results

    def calibrate(
        self,
        *,
        target_labels: Sequence[int],
        lookups: Sequence[Sequence[Lookup]],
        thresholds_targets: Mapping[str, float],
        calibration_metric: ClassificationMetric,
        matcher: Union[str, ClassificationMatch],
        extra_metrics: Sequence[ClassificationMetric] = [],
        distance_rounding: int = 8,
        metric_rounding: int = 6,
        verbose: int = 1
    ) -> CalibrationResults:
        """Computes the distances thresholds that the classification must match to
        meet a fixed target.

        Args:
            target_labels: Sequence of expected labels for the lookups.

            lookup: Sequence of lookup results as produced by the
            `Index.batch_lookup()` method.

            thresholds_targets: classification metrics thresholds that are
            targeted. The function will find the closed distance value.

            calibration_metric: Classification metric used for calibration.

            matcher: {'match_nearest', 'match_majority_vote'} or
            ClassificationMatch object. Defines the classification matching,
            e.g., match_nearest will count a True Positive if the query_label
            is equal to the label of the nearest neighbor and the distance is
            less than or equal to the distance threshold.

            extra_metrics: Additional metrics that should be computed and
            reported as part of the classification. Defaults to [].

            distance_rounding: How many digit to consider to
            decide if the distance changed. Defaults to 8.

            metric_rounding: How many digit to consider to decide if
            the metric changed. Defaults to 6.

            verbose: Be verbose. Defaults to 1.
        Returns:
            CalibrationResults containing the thresholds and cutpoints Dicts.
        """

        # making a single list of metrics
        # Need expl covariance problem
        combined_metrics = list(extra_metrics)
        combined_metrics.append(calibration_metric)

        # data preparation: flatten and rounding
        # lookups will be shape(num_queries, num_neighbors)
        # distances will be len(num_queries x num_neighbors)
        lookup_distances = unpack_lookup_distances(lookups, distance_rounding)
        lookup_labels = unpack_lookup_labels(lookups)
        # ensure the target labels are an int32 tensor
        target_labels = tf.convert_to_tensor(target_labels, dtype='int32')

        # the unique set of distance values sorted ascending
        distance_thresholds = tf.sort(
                tf.unique(
                    tf.reshape(lookup_distances, (-1))
                )[0]  # we only use the y output from tf.unique
        )

        results = self.evaluate_classification(
            query_labels=target_labels,
            lookup_labels=lookup_labels,
            lookup_distances=lookup_distances,
            distance_thresholds=distance_thresholds,
            metrics=combined_metrics,
            matcher=matcher,
            distance_rounding=distance_rounding,
            verbose=verbose)

        # pack results into one dict per dist_threshold
        # TODO(ovallis): we can likey refactor the rest of this method to
        # remove the need for this unpacking, but keeping it the same for now
        # to ensure the code is working as expected.
        evaluations = []
        for i, dist in enumerate(distance_thresholds):
            ev = {'distance': float(results['distance'][i])}
            for m in combined_metrics:
                ev[m.name] = float(results[m.name][i])

            evaluations.append(ev)

        # find the thresholds by going from right to left

        # distances are rounded because of numerical instablity
        # copy threshold targets as we are going to delete them and don't want
        # to alter users supplied data
        thresholds_targets = copy(thresholds_targets)

        # which direction metric improvement is?
        # !loop is right to left so max is decreasing and min is increasing
        if calibration_metric.direction == 'max':
            # we want the lowest value at the largest distance possible
            cmp = self._is_lower
            prev_value = math.inf  # python 3.x only
        else:
            # we want the highest value at the largest distance possible
            cmp = self._is_higher
            prev_value = 0

        # we need a collection of list to apply vectorize operations and make
        # the analysis / viz of the classification data signifcantly easier
        thresholds: DefaultDict[str, List[Union[int, float]]] = defaultdict(list)  # noqa
        cutpoints: DefaultDict[str, Dict[str, Union[str, float, int]]] = defaultdict(dict)  # noqa
        num_distances = len(distance_thresholds)

        if verbose:
            pb = tqdm(total=num_distances, desc='computing thresholds')

        # looping from right to left as we want the max distance for a given
        # metric value
        for ridx in range(num_distances):
            idx = num_distances - ridx - 1  # reversed

            # Rounding the classification metric to create bins
            curr_eval = evaluations[idx]
            classification_value = curr_eval[calibration_metric.name]
            curr_value = round(classification_value, metric_rounding)

            # ? if bug use this line check that the values evolve correclty.
            # print(curr_value, prev_value, cmp(curr_value, prev_value))

            if cmp(curr_value, prev_value):

                # add a new distance threshold
                thresholds['value'].append(curr_value)

                # ! the correct distance is already in the eval data
                # record the value for all the metrics requested by the user
                for k, v in curr_eval.items():
                    thresholds[k].append(v)

                # update current threshold value
                prev_value = curr_value

                # check if the current value meet or exceed threshold target
                to_delete = []  # can't delete in an interation loop
                for name, value in thresholds_targets.items():
                    if cmp(curr_value, value, equal=True):
                        cutpoints[name] = {'name': name}  # useful for display
                        for k in thresholds.keys():
                            cutpoints[name][k] = thresholds[k][-1]
                        to_delete.append(name)

                # removing found targets to avoid finding lower value
                # recall we go from right to left in the evaluation
                for name in to_delete:
                    del thresholds_targets[name]

            if verbose:
                pb.update()

        if verbose:
            pb.close()

        # find the optimal cutpoint
        if calibration_metric.direction == 'min':
            best_idx = tf.math.argmin(thresholds[calibration_metric.name])
        else:
            best_idx = tf.math.argmax(thresholds[calibration_metric.name])

        # record its value
        cutpoints['optimal'] = {'name': 'optimal'}  # useful for display
        for k in thresholds.keys():
            cutpoints['optimal'][k] = thresholds[k][best_idx]

        # reverse the threshold so they go from left to right as user expect
        for k in thresholds.keys():  # this syntax is need for mypy ...
            thresholds[k].reverse()

        return CalibrationResults(cutpoints=cutpoints, thresholds=thresholds)

    def _is_lower(self, curr, prev, equal=False):
        if equal:
            return curr <= prev
        return curr < prev

    def _is_higher(self, curr, prev, equal=False):
        if equal:
            return curr >= prev
        return curr > prev
