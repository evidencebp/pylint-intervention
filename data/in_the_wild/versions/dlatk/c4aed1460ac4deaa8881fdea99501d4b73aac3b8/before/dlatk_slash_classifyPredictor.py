#!/bin/python
"""
Classify Predictor

Interfaces with DLATK and scikit-learn
to perform classification of binary outcomes for lanaguage features.
"""
import pickle as pickle

import sys
import random
from itertools import combinations, zip_longest, islice
import csv

from pprint import pprint
import collections

import pandas as pd

try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable
from collections import defaultdict, Counter

# scikit-learn imports
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
    auc,
    roc_auc_score,
    matthews_corrcoef,
)
from sklearn import metrics

from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.multiclass import OneVsRestClassifier

#scikit-learn classifier imports
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression, Lasso, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

#scikit learn feature selection and reduction:
from sklearn.feature_selection import f_classif, SelectPercentile, SelectKBest, SelectFdr, SelectFpr, SelectFwe
from sklearn.decomposition import MiniBatchSparsePCA, PCA, KernelPCA, NMF, FactorAnalysis

#scikit-learn model helping: 
from sklearn.model_selection import StratifiedKFold, KFold, ShuffleSplit, train_test_split, GridSearchCV 
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score, roc_curve, auc, roc_auc_score, matthews_corrcoef
from sklearn import metrics
from sklearn.preprocessing import StandardScaler, label_binarize, MinMaxScaler
from sklearn.multiclass import OneVsRestClassifier
from sklearn.utils import shuffle
from sklearn.pipeline import Pipeline
from sklearn.base import ClassifierMixin

#scipy
from scipy.stats import zscore, t, wilcoxon

from scipy.stats.stats import pearsonr, spearmanr
from scipy.sparse import hstack
try:
    from scipy.sparse import csr_array, sparray
except ImportError as e:
    from scipy.sparse import csr_matrix as csr_array, spmatrix as sparray
import numpy as np
from numpy import sqrt, array, std, mean, int64, ceil

# infrastructure
from .mysqlmethods import mysqlMethods as mm
from .dlaConstants import DEFAULT_RANDOM_SEED, warn
from .wrappedPCA import WrappedPCA

# For ROC curves
try:
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
except:
    print("Could not import PdfPages or pyplot from matplotlib")


def alignDictsAsXy(X, y, sparse=False, returnKeyList=False, keys=None):
    """turns a list of dicts for x and a dict for y into a matrix X and vector y"""
    if not keys:
        keys = frozenset(list(y.keys()))
        if sparse:
            keys = keys.intersection([item for sublist in X for item in sublist])  # union X keys
        else:
            keys = keys.intersection(*[list(x.keys()) for x in X])  # intersect X keys
        keys = list(keys)  # to make sure it stays in order
    listy = None
    try:
        listy = [float(y[k]) for k in keys]
    except KeyError:
        print(
            "!!!WARNING: alignDictsAsXy: gid not found in y; groups are being dropped (bug elsewhere likely)!!!!"
        )
        ykeys = list(y.keys())
        keys = [k for k in keys if k in ykeys]
        listy = [float(y[k]) for k in keys]

    # Keys: list of group_ids in order.
    if sparse:
        keyToIndex = dict([(keys[i], i) for i in range(len(keys))])
        row = []
        col = []
        data = []
        # columns: features.
        for c in range(len(X)):
            column = X[c]
            for keyid, value in column.items():
                if keyid in keyToIndex:
                    row.append(keyToIndex[keyid])
                    col.append(c)
                    data.append(value)

        sparseX = csr_array((data, (row, col)), shape=(len(keys), len(X)))
        if returnKeyList:
            return (sparseX, array(listy).astype(int64), keys)
        else:
            return (sparseX, array(listy).astype(int64))

    else:
        listX = [[x[k] for x in X] for k in keys]
        if returnKeyList:
            return (array(listX), array(listy).astype(int64), keys)
        else:
            return (array(listX), array(listy).astype(int64))


def alignDictsAsy(y, *yhats, **kwargs):
    keys = None
    if keys not in kwargs:
        keys = frozenset(list(y.keys()))
        for yhat in yhats:
            keys = keys.intersection(list(yhat.keys()))
    else:
        keys = kwargs["keys"]
    listy = [y[k] for k in keys]
    listyhats = []
    for yhat in yhats:
        listyhats.append([yhat[k] for k in keys])
    return tuple([listy]) + tuple(listyhats)


def pos_neg_auc(y1, y2):
    auc = 1.0
    try:
        auc = roc_auc_score(y1, y2)
    except ValueError as err:
        print("AUC threw ValueError: %s\nbogus auc included" % str(err))
    if auc < 0.5:
        auc = auc - 1
    return auc


def computeAUC(ytrue, ypredProbs, multiclass=False, negatives=True, classes=None):
    if not classes:
        classes = list(set(ytrue))
    this_auc = 0.0
    if multiclass or len(classes) > 2:
        n_classes = len(classes)
        ytrue = label_binarize(ytrue, classes=sorted(classes))

        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        #print("Muti-AUCs:")
        for i in range(n_classes):
            try:
                fpr[i], tpr[i], _ = roc_curve(ytrue[:, i], ypredProbs[:, i])
            except:
                import pdb; pdb.set_trace();
            roc_auc[i] = auc(fpr[i], tpr[i])
            #print("  ", i, ": %.4f" % roc_auc[i]) 

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(ytrue.ravel(), ypredProbs.ravel())
        # except ValueError
        this_auc = auc(fpr["micro"], tpr["micro"])
    else:
        try:
            this_auc = roc_auc_score(ytrue, ypredProbs[:, -1])
        except ValueError as e:
            print("\nWARNING: Unable to comput a ROC_AUC: '", e, "'\n  Thus, using AUC = 0.0.\n")
            this_auc = 0.0
    if negatives and this_auc < 0.5:
        this_auc = this_auc - 1
    return this_auc


class ClassifyPredictor:
    """Interfaces with scikit-learn to perform prediction of outcomes for lanaguage features.

    Attributes
    ----------
    cvParams : dict

    modelToClassName : dict

    modelToCoeffsName : dict

    cvJobs : int

    cvFolds : int

    chunkPredictions : boolean

    maxPredictAtTime : int

    backOffPerc : float

    backOffModel : str

    featureSelectionString : str or None

    featureSelectMin : int

    featureSelectPerc : float

    testPerc : float

    randomState : int

    trainingSize : int

    Parameters
    ----------
    outcomeGetter : OutcomeGetter object

    featureGetters : list of FeatureGetter objects

    modelName : :obj:`str`, optional

    Returns
    -------
    ClassifyPredictor object
    """

    # cross validation parameters:
    cvParams = {
        'svc': [
            {'kernel': ['rbf'], 'gamma': [0.001, 0.01, 0.0001, 0.1, 0.00001, 1], 'C': [1, 10, 100, 1000, 10000, 0.1]}, 
            #{'kernel': ['rbf'], 'gamma': [0.001, 0.0001, 0.00001], 'C': [1, 10, 100, 1000, 0.1]},  #msg-level
            #{'kernel': ['rbf'], 'gamma': [0.001, 0.0001, 0.01, .1, 0.00001, 0.000001], 'C': [10, 100, 1000, 10000]},  #msg-level timediffonly
            #{'kernel': ['rbf'], 'gamma': [0.0001, 0.00001, 0.000001], 'C': [10, 1, 100]},  #swl
            #{'kernel': ['rbf'], 'gamma': [0.0001, 0.00001, 0.000001], 'C': [10, 1, 100]},  #swl
            #{'kernel': ['rbf'], 'gamma': [0.00001], 'C': [10]}, #msg-level ppf
            #{'kernel': ['rbf']}, 
            #{'kernel': ['sigmoid'], 'C': [0.01, 0.001, .1, .0001, 10, 1]},                                        
            #{'kernel': ['linear'], 'C': [100, 10, 1000, 1], 'random_state': [42]}
            ],
        'linear-svc':[
            #{'C':[0.01], 'penalty':['l2'], 'dual':[True]} #timex message-level
            #{'C':[10, 1, 0.1, 0.01, 0.001, 0.0001, 0.0025, 0.00025, 0.00001, 0.000001, 0.000025, 0.0000001, 0.0000025, 0.00000001, 0.00000025], 'loss':['l2'], 'penalty':['l2'], 'dual':[True]}, #swl
            #{'C':[100, 10, 1, 500, 1000, 5000, 10000, 25000, 0.1, 0.01, 0.001, 0.0001], 'loss':['l2'], 'penalty':['l2'], 'dual':[True]}
            #{'C':[0.0001, 0.001, 0.00001, 0.01], 'penalty':['l2'], 'dual':[True]}
            #{'C':[0.01, 0.1, 0.001, 1, 0.0001, 10, 0.00001, 0.000001, 0.0000001], 'loss':['l2'], 'penalty':['l2'], 'dual':[True]} #swl user
            #{'C':[0.01, 0.1, 0.001, 1, 0.0001, 10], 'loss':['l2'], 'penalty':['l2'], 'dual':[True]} #depression user
            #{'C':[0.01, 0.1, 0.001, 0.0001, 0.00001, 0.000001], 'loss':['l2'], 'penalty':['l2'], 'dual':[False]} #depression user lots o feats
            #{'C':[1, 100, 10, 5, 2, 0.1], 'loss':['l2'], 'penalty':['l2'], 'dual':[True]}, #topics, personality
            #{'C':[100, 10, 1000, 10000], 'loss':['l1'], 'penalty':['l2'], 'dual':[True]},
            #{'C':[1000], 'loss':['l1'], 'penalty':['l2'], 'dual':[True]},
            #{'C':[100, 10, 1000, 10000], 'loss':['l2'], 'penalty':['l1'], 'dual':[False]},
            #{'C':[100, 10, 1000, 1, 10000], 'penalty':['l1'], 'dual':[False]},
            #{'C':[100, 10, 1000, 1, 10000, .1], 'penalty':['l1'], 'dual':[False]},
            #{'C':[100, 500, 10, 1000, 5000, 1, 10000], 'loss': ['l2'], 'penalty':['l2'], 'dual':[True]},
            #{'C':[5000]},
            #{'C':[100],'penalty':['l1'], 'dual':[False]} # 1gram gender classification no standardize no featureSelection
            #{'C':[100, 10, 1000], 'penalty':['l1'], 'dual':[False]},
            #{'C':1.0, 'fit_intercept':True, 'loss':'l2', penalty:'l2'}, #if not centered data, use fit_intercept
            #{'C':1.0, 'dual':False}, #when N_samples > n_features
            #{'C':[0.01, 0.1, 1, 10, 0.001], 'penalty':['l2'], 'dual':[True]} #timex message-level

            ###with l1 feature selection:
            {'C':[0.01], 'penalty':['l1'], 'dual':[False], 'class_weight':['balanced']} #age, general sparse setting #words n phrases, gender (best 0.01=> 91.4 )
            #{'C':[0.01, 0.1, 0.001], 'penalty':['l1'], 'dual':[False], 'class_weight':['balanced']}, #FIRST PASS l1 OPTION; swl message-level
            #{'C':[10, 1, 0.1, 0.01, 0.001, 0.0001, 0.0025, 0.00025, 0.00001, 0.000001, 0.000025, 0.0000001, 0.0000025, 0.00000001, 0.00000025], 'penalty':['l1'], 'dual':[False]} #swl
            #{'C':[0.1], 'penalty':['l1'], 'dual':[False], 'multi_class':['crammer_singer']} #
            #{'C':[0.01, 0.1, 1, 10, 0.001], 'penalty':['l1'], 'dual':[False]} #timex message-level
            #{'C':[0.000001], 'penalty':['l2']}, # UnivVsMultiv choice Maarten 
            #{'C':[0.001], 'penalty':['l1'], 'dual':[False]}, # UnivVsMultiv choice Maarten 
            #{'C':[1000000], 'penalty':['l2'], 'dual':[False]} #simulate l0
            #{'C':[1, 10, 0.1, 0.01, 0.05, 0.005], 'penalty':['l1'], 'dual':[False]} #swl/perma message-level
            ],
        'lr': [
            {'C':[0.01], 'penalty':['l2'], 'dual':[False], 'random_state': [42]},#DEFAULT
            #{'C':[0.01, 0.1, 1, 10], 'penalty':['l2'], 'dual':[False]}, 
            #{'C':[0.01, 0.1, 0.001, 1], 'penalty':['l2'], 'dual':[False]}, 
            #{'C':[0.00001], 'penalty':['l2']} # UnivVsMultiv choice Maarten
            #{'C':[1000000], 'penalty':['l2'], 'dual':[False]} # for a l0 penalty approximation
            #{'C':[1000000000000], 'penalty':['l2'], 'dual':[False]} # for a l0 penalty approximation
            ##L1 
            #{'C':[0.01], 'penalty':['l1']} # DEFAULT L1
            #{'C':[0.01, 0.1, 0.001, 1, .0001, 10], 'penalty':['l1'], 'dual':[False]},
            #{'C':[0.1, 1, 0.01], 'penalty':['l1'], 'dual':[False]} #timex message-level
            #{'C':[10, 1, 100, 1000], 'penalty':['l1'], 'dual':[False]} 
            #{'C':[0.01, 0.1, 0.001, 0.0001, 0.00001], 'penalty':['l1'], 'dual':[False]}
            #{'C':[0.1, 1, 10], 'penalty':['l1'], 'dual':[False]} #timex l2 rpca....
            #{'C':[100], 'penalty':['l1'], 'dual':[False]} # gender prediction
            #{'C':[.01], 'penalty':['elasticnet'], 'dual':[False], 'random_state': [42], 'l1_ratio': [.8], 'solver': ['saga']},
            ],
        'lr1': [{'C':[1], 'penalty':['l2'], 'dual':[False], 'random_state': [42]}],
        'lr_balanced': [{'C':[0.01], 'penalty':['l2'], 'dual':[False], 'random_state': [42], 'class_weight': ['balanced']}],
        #unpenalized logistic regression:
        'lrnone': [{'C':[1000000], 'penalty':['l2'], 'dual':[False], 'random_state': [42]}],

        'etc': [ 
            #{'n_jobs': [10], 'n_estimators': [250], 'criterion':['gini']}, 
            {'n_jobs': [10], 'n_estimators': [1000], 'criterion':['gini']},  #DEFAULT
            #{'n_jobs': [10], 'n_estimators': [250], 'max_features':['log2'],'criterion':['gini']}, 
            #{'n_jobs': [12], 'n_estimators': [50], 'max_features': ["sqrt", "log2", None], 'criterion':['gini', 'entropy'], 'min_samples_split': [2]},
           # {'n_jobs': [12], 'n_estimators': [1000], 'max_features': ["sqrt"], 'criterion':['gini'], 'min_samples_split': [2], 'class_weight': ['balanced_subsample']},#BEST
            #{'n_jobs': [12], 'n_estimators': [1000], 'max_features': [None], 'criterion':['gini'], 'min_samples_split': [2], 'class_weight': ['balanced_subsample']},
            #{'n_jobs': [12], 'n_estimators': [1000], 'max_features': ["sqrt"], 'criterion':['gini'], 'min_samples_split': [2]},
            #{'n_jobs': [12], 'n_estimators': [1000], 'max_features': ["sqrt"], 'criterion':['gini'], 'min_samples_split': [2], 'class_weight': ['balanced']}, 
            #{'n_jobs': [12], 'n_estimators': [200], 'max_features': ["sqrt"], 'critearion':['gini'], 'min_samples_split': [2]}, 
            ],
        'rfc': [
            {'n_jobs': [10], 'n_estimators': [1000]}, 
            ],
        'pac': [
            {'n_jobs': [10], 'C': [1, .1, 10]}, 
            ],
        # 'lda': [
        #     {},
        #     ],
        "gbc": [
            {
                "n_estimators": [500],
                "random_state": [DEFAULT_RANDOM_SEED],
                "subsample": [0.4],
                "max_depth": [5],
            },
            # {'n_estimators': [50], 'random_state': [DEFAULT_RANDOM_SEED], 'learning_rate': [0.2], 'min_samples_leaf': [50],
            # 'subsample':[0.8], 'max_depth': list(range(5,16,2)), 'max_features': list(range(5,100,5)), },
        ],
        "mnb": [
            {"alpha": [1.0], "fit_prior": [False], "class_prior": [None]},
        ],
        "gnb": [
            {},
            # {'priors': [None]}, # 'priors' becomes a parameter in sklearn 0.18
            ], 
        'bnb': [
            {'alpha': [1.0], 'fit_prior': [False], 'binarize':[True]},
            ],
        'mlp': [ #multi-layer perceptron
            #{'alpha': [0.1, 0.001, 1.0, 0.01, 10, 100], 'solver': ['lbfgs'], 'hidden_layer_sizes':[(30,10)], 'random_state': [DEFAULT_RANDOM_SEED]},
            {'alpha': np.logspace(-1.5, 1.5, 5), 'learning_rate_init': [0.001], 'solver': ['sgd'], 'hidden_layer_sizes':[(10,10)], 'max_iter': [500], 'n_iter_no_change': [10], 'random_state': [DEFAULT_RANDOM_SEED]},
            ],
        
        }

    modelToClassName = {
        'lr' : 'LogisticRegression',
        'lr1' : 'LogisticRegression',
        'lr_balanced' : 'LogisticRegression',
        'lrnone' : 'LogisticRegression',
        'linear-svc' : 'LinearSVC',
        'svc' : 'SVC',
        'etc' : 'ExtraTreesClassifier',
        'rfc' : 'RandomForestClassifier',
        'pac' : 'PassiveAggressiveClassifier',
        #'lda' : 'LDA', #linear discriminant analysis
        'gbc' : 'GradientBoostingClassifier',
        'mnb' : 'MultinomialNB',
        'gnb' : 'GaussianNB', 
        'bnb' : 'BernoulliNB',
        'mlp' : 'MLPClassifier',
        }
    
    modelToCoeffsName = {
        ##TODO##
        'linear-svc' : 'coef_',
        'svc' : 'coef_',
        'lr': 'coef_',
        'lr1': 'coef_',
        'lrnone': 'coef_',
        'mnb': 'coef_',
        'bnb' : 'feature_log_prob_',
        'mlp' : 'coefs_',
        }

    # cvJobs = 3 #when lots of data
    # cvJobs = 6 #normal
    cvJobs = 8  # resource-heavy

    cvFolds = 3
    chunkPredictions = False  # whether or not to predict in chunks (good for keeping track when there are a lot of predictions to do)
    maxPredictAtTime = 30000
    backOffPerc = .01 #when the num_featrue / training_insts is less than this backoff to backoffmodel
    backOffModel = 'lrnone' #'lr'

    # feature selection:
    featureSelectionString = None
    # featureSelectionString = 'SelectKBest(f_classif, k=int(len(y)/3))'
    # featureSelectionString = 'SelectFdr(f_classif, alpha=0.01)' #THIS DOESNT SEEM TO WORK!
    # featureSelectionString = 'SelectFpr(f_classif)' #this is correlation feature selection
    # featureSelectionString = 'SelectFwe(f_classif, alpha=30.0)' #this is correlation feature selection w/ correction
    # featureSelectionString = 'SelectFwe(f_classif, alpha=200.0)'   ### TRY THIS ###
    # featureSelectionString = 'SelectPercentile(f_classif, 33)'#1/3 of features
    # featureSelectionString = 'ExtraTreesClassifier(n_jobs=10, n_estimators=100, compute_importances=True)'
    # featureSelectionString = \
    #    'Pipeline([("univariate_select", SelectPercentile(f_classif, 33)), ("L1_select", RandomizedLasso(random_state=42, n_jobs=self.cvJobs))])
    # featureSelectionString = 'Pipeline([("1_univariate_select", SelectFwe(f_classif, alpha=30.0)), ("2_rpca", RandomizedPCA(n_components=max(min(int(X.shape[1]*.10), int(X.shape[0]/max(1.5,len(self.featureGetters)))), min(50, X.shape[1])), random_state=42, whiten=False, iterated_power=3))])'

    # dimensionality reduction (TODO: make a separate step than feature selection)
    # featureSelectionString = 'PCA(n_components=max(min(int(X.shape[1]*.10), int(X.shape[0]/max(1.5,len(self.featureGetters)))), min(50, X.shape[1])), random_state=42, whiten=False, iterated_power=3, svd_solver="randomized")' ### TRY THIS ###
    # featureSelectionString = 'PCA(n_components=max(min(int(X.shape[1]*.10), int(X.shape[0]/len(self.featureGetters))), min(50, X.shape[1])), random_state=42, whiten=False, iterated_power=3, svd_solver="randomized")'#smaller among 10% or number of rows / number of feature tables
    # featureSelectionString = 'RandomizedPCA(n_components=max(min(int(X.shape[1]*.10), int(X.shape[0]/2)), min(50, X.shape[1])), random_state=42, whiten=False, iterated_power=3)'#smaller among 10% or number of rows / 2
    # featureSelectionString = 'RandomizedPCA(n_components=min(X.shape[1], int(X.shape[0]/4)), random_state=42, whiten=False, iterated_power=3)'
    # featureSelectionString = 'RandomizedPCA(n_components=min(X.shape[1], 2000), random_state=42, whiten=False, iterated_power=3)'
    # featureSelectionString = 'RandomizedPCA(n_components=int(X.shape[1]*.10), random_state=42, whiten=False, iterated_power=3)'
    # featureSelectionString = 'RandomizedPCA(n_components=min(int(X.shape[0]*1.5), X.shape[1]), random_state=42, whiten=False, iterated_power=3)'
    # featureSelectionString = 'PCA(n_components=min(int(X.shape[1]*.10), X.shape[0]), whiten=False)'
    # featureSelectionString = 'PCA(n_components=0.99, whiten=False)'
    # featureSelectionString = 'KernelPCA(n_components=int(X.shape[1]*.02), kernel="rbf", degree=3, eigen_solver="auto")'

    featureSelectMin = 50  # must have at least this many features to perform feature selection
    featureSelectPerc = (
        1.00  # only perform feature selection on a sample of training (set to 1 to perform on all)
    )
    # featureSelectPerc = 0.20 #only perform feature selection on a sample of training (set to 1 to perform on all)

    testPerc = 0.20  # percentage of sample to use as test set (the rest is training)
    randomState = (
        DEFAULT_RANDOM_SEED  # percentage of sample to use as test set (the rest is training)
    )
    # randomState = 64 #percentage of sample to use as test set (the rest is training)

    trainingSize = (
        1000000  # if this is smaller than the training set, then it will be reduced to this.
    )

    def __init__(self, og, fgs, modelName="svc", outliersToMean=None, n_components=None):
        # initialize classification predictor
        self.outcomeGetter = og

        # setup feature getters:

        if not isinstance(fgs, Iterable):
            fgs = [fgs]
        self.featureGetters = fgs
        self.featureGetter = fgs[0]  # legacy support

        # setup other params / instance vars
        self.modelName = modelName
        """str: Docstring *after* attribute, with type specified."""

        self.classificationModels = dict()
        """dict: Docstring *after* attribute, with type specified."""

        self.scalers = dict()
        """dict: Docstring *after* attribute, with type specified."""

        self.fSelectors = dict()
        """dict: Docstring *after* attribute, with type specified."""

        self.outcomeNames = []
        """list: Holds a list of the outcomes in sorted order."""

        self.n_components = n_components  # number of components for feature selection
        """int: Docstring *after* attribute, with type specified."""

        self.featureNames = []
        """list: Holds the order the features are expected in."""

        self.featureLengthDict = dict()
        """dict: Holds the number of features in each featureGetter."""

        self.featureNamesList = []
        """list: Holds the names of features in each featureGetter."""

        self.multiFSelectors = None
        """str: Docstring *after* attribute, with type specified."""

        self.multiScalers = None
        """str: Docstring *after* attribute, with type specified."""

        self.multiXOn = False
        """boolean: whether multiX was used for training."""

        self.outliersToMean = outliersToMean
        """float: Threshold for setting outliers to mean value."""

        self.trainBootstrapNames = None

    def train(
        self,
        standardize=True,
        sparse=False,
        restrictToGroups=None,
        groupsWhere="",
        trainBootstraps=None,
        trainBootstrapsNs=None,
    ):
        """Tests classifier, by pulling out random testPerc percentage as a test set"""

        ################
        # 1. setup groups
        (groups, allOutcomes, allControls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )
        if restrictToGroups:  # restrict to groups
            rGroups = restrictToGroups
            if isinstance(restrictToGroups, dict):
                rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
            groups = groups.intersection(rGroups)
            for outcomeName, outcomes in allOutcomes.items():
                allOutcomes[outcomeName] = dict(
                    [(g, outcomes[g]) for g in groups if (g in outcomes)]
                )
            for controlName, controlValues in controls.items():
                controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        print("[number of groups: %d]" % (len(groups)))

        ####################
        # 2. get data for Xs:
        (groupNormsList, featureNamesList, featureLengthList) = ([], [], [])
        XGroups = None  # holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        UGroups = None
        for fg in self.featureGetters:
            (groupNorms, featureNames) = fg.getGroupNormsSparseFeatsFirst(groups)
            groupNormValues = [
                groupNorms[feat] for feat in featureNames
            ]  # list of dictionaries of group_id => group_norm
            groupNormsList.append(groupNormValues)
            # print featureNames[:10]#debug
            featureNamesList.append(featureNames)
            featureLengthList.append(len(featureNames))
            fgGroups = getGroupsFromGroupNormValues(groupNormValues)
            if not XGroups:
                XGroups = set(fgGroups)
                UGroups = set(fgGroups)
            else:
                XGroups = XGroups & fgGroups  # intersect groups from all feature tables
                UGroups = UGroups | fgGroups  # intersect groups from all feature tables
                # potential source of bug: if a sparse feature table doesn't have all the groups it should

        XGroups = (
            XGroups | groups
        )  # probably unnecessary since groups was given when grabbing features (in which case one could just use groups)
        UGroups = (
            UGroups | groups
        )  # probably unnecessary since groups was given when grabbing features (in which case one could just use groups)

        ################################
        # 2b) setup control data:
        controlValues = list(allControls.values())
        if controlValues:
            groupNormsList.append(controlValues)

        #########################################
        # 3. train for all possible ys:
        self.multiXOn = True
        if trainBootstraps:
            self.trainBootstrapNames = dict()
        (self.classificationModels, self.multiScalers, self.multiFSelectors) = (
            dict(),
            dict(),
            dict(),
        )
        for outcomeName, outcomes in sorted(allOutcomes.items()):
            self.outcomeNames.append(outcomeName)
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            multiXtrain = list()
            # trainGroupsOrder = list(XGroups & set(outcomes.keys()))
            trainGroupsOrder = list(UGroups & set(outcomes.keys()))
            for i in range(len(groupNormsList)):
                groupNormValues = groupNormsList[i]
                # featureNames = featureNameList[i] #(if needed later, make sure to add controls to this)
                (Xdicts, ydict) = (groupNormValues, outcomes)
                print("  (feature group: %d)" % (i))
                (Xtrain, ytrain) = alignDictsAsXy(Xdicts, ydict, sparse=True, keys=trainGroupsOrder)
                if len(ytrain) > self.trainingSize:
                    Xtrain, Xthrowaway, ytrain, ythrowaway = train_test_split(
                        Xtrain,
                        ytrain,
                        test_size=len(ytrain) - self.trainingSize,
                        random_state=self.randomState,
                    )
                multiXtrain.append(Xtrain)
                print("   [Train size: %d ]" % (len(ytrain)))

            #############
            # 4) fit model
            (
                self.classificationModels[outcomeName],
                self.multiScalers[outcomeName],
                self.multiFSelectors[outcomeName],
            ) = self._multiXtrain(multiXtrain, ytrain, standardize, sparse=sparse)

            if trainBootstraps:
                # create a set of bootstrapped training instances (usually to be exported in separate pickles)
                print(
                    "Running Bootstrapoped Trainined for %s, %d resamples"
                    % (outcomeName, trainBootstraps)
                )
                if not trainBootstrapsNs:
                    trainBootstrapsNs = [len(ytrain)]
                self.trainBootstrapNames[outcomeName] = {}  # saves all of the outcome names
                for sampleN in sorted(trainBootstrapsNs, reverse=True):
                    bsBaseOutcomeName = outcomeName + "_N" + str(sampleN)
                    # TODO: sample N
                    bsi = 0
                    self.trainBootstrapNames[outcomeName][sampleN] = []
                    for bsMultiX, bsY in self._monteCarloResampleMultiXY(
                        multiXtrain, ytrain, trainBootstraps, sampleN=sampleN
                    ):
                        print("Sample Size: %d, bs resample num: %d" % (sampleN, bsi))
                        bsOutcomeName = bsBaseOutcomeName + "_bs" + str(bsi)
                        self.trainBootstrapNames[outcomeName][sampleN].append(bsOutcomeName)
                        (
                            self.classificationModels[bsOutcomeName],
                            self.multiScalers[bsOutcomeName],
                            self.multiFSelectors[bsOutcomeName],
                        ) = self._multiXtrain(bsMultiX, bsY, standardize, sparse=False)
                        bsi += 1

        print("\n[TRAINING COMPLETE]\n")
        self.featureNamesList = featureNamesList
        # coefficients = eval('self.classificationModels["page_edits_post_abs_a"].%s' % self.modelToCoeffsName[self.modelName.lower()])

    def test(
        self, standardize=True, sparse=False, saveModels=False, blacklist=None, groupsWhere=""
    ):
        """Tests classifier, by pulling out random testPerc percentage as a test set"""

        print()
        print("USING BLACKLIST: %s" % str(blacklist))
        # 1. get data possible ys (outcomes)
        (groups, allOutcomes, controls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )
        print("[number of groups: %d]" % len(groups))

        # 2. get data for X:
        (groupNorms, featureNames) = (None, None)
        if len(self.featureGetters) > 1:
            print(
                "\n!!! WARNING: multiple feature tables passed in rp.test only handles one for now.\n        try --combo_test_classification or --predict_classification !!!\n"
            )
        if sparse:
            if blacklist:
                print("\n!!!WARNING: USING BLACKLIST WITH SPARSE IS NOT CURRENTLY SUPPORTED!!!\n")
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsSparseFeatsFirst(groups)
        else:
            if blacklist:
                print("USING BLACKLIST: %s" % str(blacklist))
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsWithZerosFeatsFirst(
                groups, blacklist=blacklist
            )
        groupNormValues = list(groupNorms.values())  # list of dictionaries of group => group_norm
        controlValues = list(controls.values())  # list of dictionaries of group=>group_norm
        #     this will return a dictionary of dictionaries

        # 3. test classifiers for each possible y:
        for outcomeName, outcomes in sorted(allOutcomes.items()):
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            (X, y) = alignDictsAsXy(groupNormValues + controlValues, outcomes, sparse)
            print("[Initial size: %d]" % len(y))
            Xtrain, Xtest, ytrain, ytest = train_test_split(
                X, y, test_size=self.testPerc, random_state=self.randomState
            )
            if len(ytrain) > self.trainingSize:
                Xtrain, Xthrowaway, ytrain, ythrowaway = train_test_split(
                    Xtrain,
                    ytrain,
                    test_size=len(ytrain) - self.trainingSize,
                    random_state=self.randomState,
                )
            print("[Train size: %d    Test size: %d]" % (len(ytrain), len(ytest)))

            (classifier, scaler, fSelector) = self._train(Xtrain, ytrain, standardize)
            ypred = self._predict(classifier, Xtest, scaler=scaler, fSelector=fSelector)
            R2 = metrics.r2_score(ytest, ypred)
            # R2 = r2simple(ytest, ypred)
            print("*R^2 (coefficient of determination): %.4f" % R2)
            print("*R (sqrt R^2):                       %.4f" % sqrt(R2))
            # ZR2 = metrics.r2_score(zscore(list(ytest)), zscore(list(ypred)))
            # print "*Standardized R^2 (coef. of deter.): %.4f"% ZR2
            # print "*Standardized R (sqrt R^2):          %.4f"% sqrt(ZR2)
            print("*Pearson r:                          %.4f (p = %.5f)" % pearsonr(ytest, ypred))
            print("*Spearman rho:                       %.4f (p = %.5f)" % spearmanr(ytest, ypred))
            mse = metrics.mean_squared_error(ytest, ypred)
            print("*Mean Squared Error:                 %.4f" % mse)
            # print "*Root Mean Squared Error:            %.5f"% sqrt(float(mse))
            if saveModels:
                (
                    self.classificationModels[outcomeName],
                    self.scalers[outcomeName],
                    self.fSelectors[outcomeName],
                ) = (classifier, scaler, fSelector)

        print("\n[TEST COMPLETE]\n")

    #####################################################
    ######## Main Testing Method ########################
    def testControlCombos(
        self,
        standardize=True,
        sparse=False,
        saveModels=False,
        blacklist=None,
        noLang=False,
        allControlsOnly=False,
        comboSizes=None,
        nFolds=2,
        savePredictions=False,
        weightedEvalOutcome=None,
        stratifyFolds=True,
        adaptTables=None,
        adaptColumns=None,
        controlCombineProbs=True,
        groupsWhere="",
        testFolds=None,
    ):
        """Tests classifier, by pulling out random testPerc percentage as a test set"""  # edited by Youngseo

        ###################################
        # 1. setup groups for random folds
        if blacklist:
            print("USING BLACKLIST: %s" % str(blacklist))
        (groups, allOutcomes, allControls, foldLabels) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere, includeFoldLabels=True
        )
        groupFolds = []
        if foldLabels:
            print("    ***explicit fold labels specified, not splitting or stratifying again***")
            stratifyFolds = False
            temp = {}
            for k, v in sorted(foldLabels.items()):
                temp.setdefault(v, []).append(k)
            groupFolds = list(temp.values())
            nFolds = len(groupFolds)
        elif not stratifyFolds:
            print(
                "[number of groups: %d (%d Folds)] non-stratified / using same folds for all outcomes"
                % (len(groups), nFolds)
            )
            random.seed(self.randomState)
            groupList = list(groups)
            random.shuffle(groupList)
            groupFolds = foldN(groupList, nFolds)
        else:
            # stratification happens on an outcome by outcome basis (lower in the code)
            print("    using stratified folds; different folds per outcome")

        ####
        # 1a: setup weightedEval
        wOutcome = None
        if weightedEvalOutcome:
            try:
                wOutcome = allOutcomes[weightedEvalOutcome]
                del allOutcomes[weightedEvalOutcome]
            except KeyError:
                print(
                    "Must specify weighted eval outcome as a regular outcome in order to get data."
                )
                sys.exit(1)

        ####################
        # 2. get data for Xs:
        (groupNormsList, featureNamesList) = ([], [])
        XGroups = None  # (intersect) holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        UGroups = None  # (union) holds the set of groups from any feature table
        for fg in self.featureGetters:
            # (groupNorms, featureNames) = (None, None)
            if blacklist:
                print("!!!WARNING: USING BLACKLIST WITH SPARSE IS NOT CURRENTLY SUPPORTED!!!")
            (groupNorms, featureNames) = fg.getGroupNormsSparseFeatsFirst(groups)
            groupNormValues = list(
                groupNorms.values()
            )  # list of dictionaries of group_id => group_norm
            groupNormsList.append(groupNormValues)
            featureNamesList.append(featureNames)
            fgGroups = getGroupsFromGroupNormValues(groupNormValues)
            if not XGroups:
                XGroups = set(fgGroups)
                UGroups = set(fgGroups)
            else:
                XGroups = XGroups & fgGroups  # intersect groups from all feature tables
                UGroups = UGroups | fgGroups  # intersect groups from all feature tables
                # potential source of bug: if a sparse feature table doesn't have all the groups it should
        XGroups = (
            XGroups & groups
        )  # probably unnecessary since groups was given when grabbing features (in which case one could just use groups)
        UGroups = UGroups & groups

        ################################
        # 2b) setup control combinations:
        controlKeys = list(allControls.keys())
        scores = (
            dict()
        )  # outcome => control_tuple => [0],[1] => scores= {R2, R, r, r-p, rho, rho-p, MSE, train_size, test_size, num_features,yhats}
        if not comboSizes:
            comboSizes = range(len(controlKeys)+1)
            if allControlsOnly  and len(controlKeys) > 0:
                #if len(controlKeys) > 1: 
                #    comboSizes = [0, 1, len(controlKeys)]
                # else:
                comboSizes = [0, len(controlKeys)]
        for r in comboSizes:
            for controlKeyCombo in combinations(controlKeys, r):
                controls = dict()
                if len(controlKeyCombo) > 0:
                    controls = dict([(k, allControls[k]) for k in controlKeyCombo])
                controlKeyCombo = tuple(controlKeyCombo)
                print("\n\n|COMBO: %s|" % str(controlKeyCombo))
                print("=" * (len(str(controlKeyCombo)) + 9))
                controlValues = list(controls.values())  # list of dictionaries of group=>group_norm
                thisGroupNormsList = list(groupNormsList)
                if controlValues:
                    thisGroupNormsList.append(controlValues)

                #########################################
                # 3. test classifiers for each possible y:
                for outcomeName, outcomes in sorted(allOutcomes.items()):
                    multiclass = False
                    # thisOutcomeGroups = set(outcomes.keys()) & XGroups #this intersects with XGroups maybe use UGroups?
                    thisOutcomeGroups = (
                        set(outcomes.keys()) & UGroups
                    )  # this intersects with UGroups
                    if not outcomeName in scores:
                        scores[outcomeName] = dict()

                    if stratifyFolds:
                        # even classes across the outcomes
                        # stratification happens within outcomes unlike foldLabels
                        print(
                            "Warning: Stratifying outcome classes across folds (thus, folds will differ across outcomes)."
                        )
                        groupFolds = stratifyGroups(
                            thisOutcomeGroups, outcomes, nFolds, randomState=DEFAULT_RANDOM_SEED
                        )
                        ##DEBUG: below is using random folds to do bootstrapping; should change back to above.
                        # print("Warning: using random folds for bootstrapping; classifyPredictor.py to fix")
                        # groupFolds = stratifyGroups(thisOutcomeGroups, outcomes, nFolds, randomState = np.random.randint(0, 10000))
                        # del groupFolds[np.random.randint(0, len(groupFolds))]

                    # for warmStartControls or controlCombinedProbs
                    lastClassifiers = [None] * nFolds
                    savedControlYpp = None
                    savedControlPProbs = None

                    for withLanguage in range(2):
                        if withLanguage:
                            if noLang or (
                                allControlsOnly and (r > 1) and (r < len(controlKeys))
                            ):  # skip to next
                                continue
                            print(
                                "\n= %s (w/ lang.)=\n%s"
                                % (outcomeName, "-" * (len(outcomeName) + 14))
                            )
                        elif controlValues:
                            print(
                                "\n= %s (NO lang.)=\n%s"
                                % (outcomeName, "-" * (len(outcomeName) + 14))
                            )
                        else:  # no controls in this iteration
                            continue

                        testStats = {
                            "acc": [],
                            "f1": [],
                            "precision": [],
                            "rho": [],
                            "rho-p": [],
                            "recall": [],
                            "mfclass_acc": [],
                            "auc": [],
                        }
                        if wOutcome:
                            testStats.update({"r-wghtd": [], "r-wghtd-p": []})
                        predictions = {}
                        predictionProbs = {}

                        ###############################
                        # 3a) iterate over nfold groups:
                        for testChunk in [
                            i for i in range(0, len(groupFolds)) if not testFolds or i in testFolds
                        ]:
                            trainGroups = set()
                            for chunk in groupFolds[:testChunk] + groupFolds[(testChunk + 1) :]:
                                trainGroups.update(chunk)
                            testGroups = set(groupFolds[testChunk])
                            # set static group order across features:
                            trainGroupsOrder = list(thisOutcomeGroups & trainGroups)
                            testGroupsOrder = list(thisOutcomeGroups & testGroups)
                            testSize = len(testGroupsOrder)
                            print("\nFold %d " % (testChunk))

                            ###########################################################################
                            # 3b)setup train and test data (different X for each set of groupNormValues)
                            (multiXtrain, multiXtest, ytrain, ytest) = (
                                [],
                                [],
                                None,
                                None,
                            )  # ytrain, ytest should be same across tables
                            # get the group order across all
                            gnListIndices = list(range(len(thisGroupNormsList)))
                            num_feats = 0
                            if not withLanguage:
                                gnListIndices = [gnListIndices[-1]]
                            for i in gnListIndices:
                                groupNormValues = thisGroupNormsList[i]
                                # featureNames = featureNameList[i] #(if needed later, make sure to add controls to this)
                                (Xdicts, ydict) = (groupNormValues, outcomes)
                                print(
                                    "   (feature group: %d): [Initial size: %d]" % (i, len(ydict))
                                )
                                (Xtrain, ytrain) = alignDictsAsXy(
                                    Xdicts, ydict, sparse=True, keys=trainGroupsOrder
                                )
                                (Xtest, ytest) = alignDictsAsXy(
                                    Xdicts, ydict, sparse=True, keys=testGroupsOrder
                                )

                                assert (
                                    len(ytest) == testSize
                                ), "ytest not the right size (%d versus %d)" % (
                                    len(ytest),
                                    testSize,
                                )
                                if len(ytrain) > self.trainingSize:
                                    Xtrain, Xthrowaway, ytrain, ythrowaway = train_test_split(
                                        Xtrain,
                                        ytrain,
                                        test_size=len(ytrain) - self.trainingSize,
                                        random_state=self.randomState,
                                    )
                                num_feats += Xtrain.shape[1]
                                multiXtrain.append(Xtrain)
                                multiXtest.append(Xtest)
                            print("[Train size: %d    Test size: %d]" % (len(ytrain), len(ytest)))

                            ################################
                            # 4) fit model and test accuracy:

                            mfclass = Counter(ytrain).most_common(1)[0][0]
                            classes = list(set(ytrain))
                            if len(classes) > 2:
                                multiclass = True
                            # Check if the classifier is using controls - Youngseo
                            if len(controls) > 0:
                                (classifier, multiScalers, multiFSelectors) = self._multiXtrain(
                                    multiXtrain,
                                    ytrain,
                                    standardize=standardize,
                                    sparse=sparse,
                                    adaptTables=adaptTables,
                                    adaptColumns=adaptColumns,
                                    classes=classes,
                                )
                                ypredProbs, ypredClasses = self._multiXpredict(
                                    classifier,
                                    multiXtest,
                                    multiScalers=multiScalers,
                                    multiFSelectors=multiFSelectors,
                                    sparse=sparse,
                                    probs=True,
                                    adaptTables=adaptTables,
                                    adaptColumns=adaptColumns,
                                )
                            else:
                                (classifier, multiScalers, multiFSelectors) = self._multiXtrain(
                                    multiXtrain,
                                    ytrain,
                                    standardize=standardize,
                                    sparse=sparse,
                                    adaptTables=None,
                                    adaptColumns=None,
                                    classes=classes,
                                )
                                ypredProbs, ypredClasses = self._multiXpredict(
                                    classifier,
                                    multiXtest,
                                    multiScalers=multiScalers,
                                    multiFSelectors=multiFSelectors,
                                    sparse=sparse,
                                    probs=True,
                                    adaptTables=None,
                                    adaptColumns=None,
                                )

                            ypred = ypredClasses[ypredProbs.argmax(axis=1)]
                            predictions.update(dict(zip(testGroupsOrder, ypred)))
                            predictionProbs.update(dict(zip(testGroupsOrder, ypredProbs)))

                            acc = accuracy_score(ytest, ypred)
                            f1 = f1_score(ytest, ypred, average="macro")
                            # auc = pos_neg_auc(ytest, ypredProbs[:,-1])
                            auc = computeAUC(
                                ytest, ypredProbs, multiclass, negatives=False, classes=classes
                            )
                            # classes = list(set(ytest))
                            # ytest_binary = label_binarize(ytest,classes=classes)
                            # ypred_binary = label_binarize(ypred,classes=classes)
                            # auc = roc_auc_score(ytest_binary, ypred_binary)
                            testCounter = Counter(ytest)
                            mfclass_acc = testCounter[mfclass] / float(len(ytest))
                            print(" *confusion matrix: \n%s" % str(confusion_matrix(ytest, ypred)))
                            print(
                                " *precision and recall: \n%s" % classification_report(ytest, ypred)
                            )
                            print(
                                " *FOLD ACC: %.4f (mfclass_acc: %.4f); mfclass: %s; auc: %.4f\n"
                                % (acc, mfclass_acc, str(mfclass), auc)
                            )
                            testStats["acc"].append(acc)
                            testStats["f1"].append(f1)
                            testStats["auc"].append(auc)
                            (rho, rho_p) = spearmanr(ytest, ypred)
                            testStats["rho"].append(rho)
                            testStats["rho-p"].append(rho_p)
                            testStats["precision"].append(
                                precision_score(ytest, ypred, average="macro")
                            )
                            testStats["recall"].append(recall_score(ytest, ypred, average="macro"))
                            testStats["mfclass_acc"].append(mfclass_acc)
                            testStats.update(
                                {
                                    "train_size": len(ytrain),
                                    "test_size": len(ytest),
                                    "num_features": num_feats,
                                    "{model_desc}": str(classifier)
                                    .replace("\t", "  ")
                                    .replace("\n", " ")
                                    .replace("  ", " "),
                                    "{modelFS_desc}": str(multiFSelectors[0])
                                    .replace("\t", "  ")
                                    .replace("\n", " ")
                                    .replace("  ", " "),
                                    "mfclass": str(mfclass),
                                    "num_classes": str(len(list(testCounter.keys()))),
                                }
                            )
                            ##4 b) weighted eval
                            if wOutcome:
                                weights = [float(wOutcome[k]) for k in testGroupsOrder]
                                try:
                                    results = sm.WLS(
                                        zscore(ytest), zscore(ypred), weights
                                    ).fit()  # runs classification
                                    testStats["r-wghtd"].append(results.params[-1])
                                    testStats["r-wghtd-p"].append(results.pvalues[-1])
                                    # print results.summary(outcomeName, [outcomeName+'_pred'])#debug
                                except ValueError as err:
                                    print(
                                        "WLS threw ValueError: %s\nresult not included" % str(err)
                                    )

                        #########################
                        # 5) aggregate test stats:
                        reportStats = dict()
                        for k, v in list(testStats.items()):
                            if isinstance(v, list):
                                reportStats["folds_" + k] = mean(v)
                                reportStats["folds_se_" + k] = std(v) / sqrt(float(nFolds))
                            else:
                                reportStats[k] = v

                        # overall stats:
                        ytrue, ypred, ypredProbs = alignDictsAsy(
                            outcomes, predictions, predictionProbs
                        )
                        ypredProbs = array(ypredProbs)
                        reportStats['acc'] = accuracy_score(ytrue, ypred)
                        reportStats['f1'] = f1_score(ytrue, ypred, average='macro')
                        reportStats['f1_weighted'] = f1_score(ytrue, ypred, average='weighted')
                        reportStats['auc']= computeAUC(ytrue, ypredProbs, multiclass,  classes = classes)
                        reportStats['auc_p'] = permutation_1tail_on_aucs(ytrue, np.array(ypredProbs), multiclass, classes)
                        reportStats['precision'] = precision_score(ytrue, ypred, average='macro')
                        reportStats['recall'] = recall_score(ytrue, ypred, average='macro')
                        reportStats['recall_micro'] = recall_score(ytrue, ypred, average='micro')
                        if not multiclass:
                            reportStats["recall_sensitivity"] = recall_score(
                                ytrue, ypred, average="binary"
                            )
                            reportStats["recall_specificity"] = recall_score(
                                np.abs(np.array(ytrue) - 1),
                                np.abs(np.array(ypred) - 1),
                                average="binary",
                            )

                        try:
                            reportStats["matt_ccoef"] = matthews_corrcoef(ytrue, ypred)
                        except ValueError as e:
                            warn("matt_ccoef: %s" % e)
                            reportStats["matt_ccoef"] = "multiclass"
                        testCounter = Counter(ytrue)
                        reportStats['mfclass_acc'] = testCounter[mfclass] / float(len(ytrue))

                        if controlCombineProbs:#ensemble with controls (AUC weighted)
                            reportStats['auc_p_v_cntrls'] = 1.0
                            reportStats['auc_cntl_comb2'] = 0.0#add columns so csv always has same
                            reportStats['auc_cntl_comb2_t'] = 0.0
                            reportStats['auc_cntl_comb2_p'] = 1.0
                            if withLanguage and savedControlYpp is not None:
                                print("\n    calculating p-values versus controls...")
                                #add lang only auc-p to top result
                                langOnlyScores = scores[outcomeName][()][1]
                                try:
                                    cntrlYtrue, YPredProbs, YCntrlProbs = alignDictsAsy(outcomes, langOnlyScores['predictionProbs'], savedControlPProbs)
                                    #langOnlyScores['auc_p_v_cntrls'] = paired_bootstrap_1tail_on_aucs(np.array(YPredProbs)[:,-1], np.array(YCntrlProbs)[:,-1], cntrlYtrue, multiclass, classes)
                                    langOnlyScores['auc_p_v_cntrls'] = paired_bootstrap_1tail_on_aucs(np.array(YPredProbs), np.array(YCntrlProbs), cntrlYtrue, multiclass, classes)
                                except KeyError:
                                    print("unable to find saved lang only probabilities")
                                    #pprint(langOnlyScores)
                                #straight up auc, p value:
                                cntrlYtrue, YPredProbs, YCntrlProbs = alignDictsAsy(outcomes, predictionProbs, savedControlPProbs)
                                #reportStats['auc_p_v_cntrls'] = paired_bootstrap_1tail_on_aucs(np.array(YPredProbs)[:,-1], np.array(YCntrlProbs)[:,-1], cntrlYtrue, multiclass, classes)
                                reportStats['auc_p_v_cntrls'] = paired_bootstrap_1tail_on_aucs(np.array(YPredProbs), np.array(YCntrlProbs), cntrlYtrue, multiclass, classes)
                                #ensemble auc: 
                                newProbsDict = ensembleNFoldAUCWeight(outcomes, [predictionProbs, savedControlPProbs], groupFolds)
                                ensYtrue, ensYPredProbs, ensYCntrlProbs = alignDictsAsy(outcomes, newProbsDict, savedControlPProbs)
                                #reportStats['auc_cntl_comb2'] = pos_neg_auc(ensYtrue, np.array(ensYPredProbs)[:,-1])
                                reportStats['auc_cntl_comb2'] = computeAUC(ensYtrue, np.array(ensYPredProbs), multiclass,  classes = classes)
                                #reportStats['auc_cntl_comb2_t'], reportStats['auc_cntl_comb2_p'] = paired_t_1tail_on_errors(np.array(ensYPredProbs)[:,-1], np.array(ensYCntrlProbs)[:,-1], ensYtrue)
                                #reportStats['auc_cntl_comb2_p'] = paired_bootstrap_1tail_on_aucs(np.array(ensYPredProbs)[:,-1], np.array(ensYCntrlProbs)[:,-1], ensYtrue, multiclass, classes)
                                reportStats['auc_cntl_comb2_p'] = paired_bootstrap_1tail_on_aucs(np.array(ensYPredProbs), np.array(ensYCntrlProbs), ensYtrue, multiclass, classes)
                                ## TODO: finish this and add flag: --ensemble_controls
                                # predictions = #todo:dictionary
                                # predictionProbs = newProbsDict
                            else:  # save probs for next round
                                savedControlYpp = ypredProbs[:, -1]
                                savedControlPProbs = predictionProbs

                        if savePredictions: 
                            reportStats['predictions'] = predictions
                            #reportStats['predictionProbs'] = {k:v[-1] for k,v in predictionProbs.items()}
                            reportStats['predictionProbs'] = predictionProbs
                        #pprint(reportStats) #debug
                        mfclass = Counter(ytest).most_common(1)[0][0]
                        print(
                            "* Overall Fold Acc: %.4f (+- %.4f) vs. MFC Accuracy: %.4f (based on test rather than train)"
                            % (
                                reportStats["folds_acc"],
                                reportStats["folds_se_acc"],
                                reportStats["folds_mfclass_acc"],
                            )
                        )
                        print(
                            "*       Overall F1: %.4f (+- %.4f)"
                            % (reportStats["folds_f1"], reportStats["folds_se_f1"])
                        )
                        print(
                            "       + precision: %.4f (+- %.4f)"
                            % (reportStats["folds_precision"], reportStats["folds_se_precision"])
                        )
                        print(
                            "       +    recall: %.4f (+- %.4f)"
                            % (reportStats["folds_recall"], reportStats["folds_se_recall"])
                        )
                        if saveModels:
                            print("!!SAVING MODELS NOT IMPLEMENTED FOR testControlCombos!!")
                        try:
                            scores[outcomeName][controlKeyCombo][withLanguage] = reportStats
                        except KeyError:
                            scores[outcomeName][controlKeyCombo] = {withLanguage: reportStats}

        print("\n[TEST COMPLETE]\n")
        return scores

    #################################################
    #################################################

    def predict(
        self, standardize=True, sparse=False, restrictToGroups=None, groupsWhere="", probs=False
    ):

        if not self.multiXOn:
            print("model trained without multiX, reverting to old predict")
            return self.old_predict(standardize, sparse, restrictToGroups)

        ################
        # 1. setup groups
        (groups, allOutcomes, allControls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )
        if restrictToGroups:  # restrict to groups
            rGroups = restrictToGroups
            if isinstance(restrictToGroups, dict):
                rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
            groups = groups.intersection(rGroups)
            for outcomeName, outcomes in allOutcomes.items():
                allOutcomes[outcomeName] = dict(
                    [(g, outcomes[g]) for g in groups if (g in outcomes)]
                )
            for controlName, controlValues in allControls.items():
                controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        print("[number of groups: %d]" % (len(groups)))

        ####################
        # 2. get data for Xs:
        groupNormsList = []
        XGroups = None  # holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        UGroups = None
        for i in range(len(self.featureGetters)):
            fg = self.featureGetters[i]
            (groupNorms, newFeatureNames) = fg.getGroupNormsSparseFeatsFirst(groups)

            print(" [Aligning current X with training X: feature group: %d]" % i)
            groupNormValues = []
            # print self.featureNamesList[i][:10]#debug
            for feat in self.featureNamesList[i]:
                if feat in groupNorms:
                    groupNormValues.append(groupNorms[feat])
                else:
                    groupNormValues.append(dict())
            groupNormsList.append(groupNormValues)
            print("  Features Aligned: %d" % len(groupNormValues))
            fgGroups = getGroupsFromGroupNormValues(groupNormValues)
            print("  Groups Aligned: %d" % len(fgGroups))
            if not XGroups:
                XGroups = set(fgGroups)
                UGroups = set(fgGroups)
            else:
                XGroups = XGroups & fgGroups  # intersect groups from all feature tables
                UGroups = UGroups | fgGroups  # intersect groups from all feature tables
                # potential source of bug: if a sparse feature table doesn't have all the groups it should
                # potential source of bug: if a sparse feature table doesn't have all of the groups which it should
        # XGroups = XGroups & groups #this should not be needed
        if len(XGroups) < len(groups):
            print(" Different number of groups available for different outcomes.")

        ################################
        # 2b) setup control data:
        controlValues = list(allControls.values())
        if controlValues:
            groupNormsList.append(controlValues)

        #########################################
        # 3. predict for all possible outcomes
        predictions = dict()
        testGroupsOrder = list(UGroups)
        # testGroupsOrder = list(XGroups)
        for outcomeName, outcomes in sorted(allOutcomes.items()):
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            if isinstance(restrictToGroups, dict):  # outcome specific restrictions:
                outcomes = dict(
                    [(g, o) for g, o in outcomes.items() if g in restrictToGroups[outcomeName]]
                )
            thisTestGroupsOrder = [gid for gid in testGroupsOrder if gid in outcomes]
            if len(thisTestGroupsOrder) < len(testGroupsOrder):
                print(
                    "   this outcome has less groups. Shrunk groups to %d total."
                    % (len(thisTestGroupsOrder))
                )
            (multiXtest, ytest) = ([], None)
            for i in range(len(groupNormsList)):  # get each feature group data (i.e. feature table)
                groupNormValues = groupNormsList[i]
                (Xdicts, ydict) = (groupNormValues, outcomes)
                print("  (feature group: %d)" % (i))
                (Xtest, ytest) = alignDictsAsXy(
                    Xdicts, ydict, sparse=True, keys=thisTestGroupsOrder
                )
                multiXtest.append(Xtest)

                print("   [Test size: %d ]" % (len(ytest)))

            #############
            # 4) predict
            if probs:
                ypredProbs, ypredClasses = self._multiXpredict(
                    self.classificationModels[outcomeName],
                    multiXtest,
                    multiScalers=self.multiScalers[outcomeName],
                    multiFSelectors=self.multiFSelectors[outcomeName],
                    sparse=sparse,
                    probs=probs,
                )
                ypred = ypredClasses[ypredProbs.argmax(axis=1)]
                ypredProbsMaxClass = ypredProbs[:, ypredClasses.argmax()]
            else:
                ypred = self._multiXpredict(
                    self.classificationModels[outcomeName],
                    multiXtest,
                    multiScalers=self.multiScalers[outcomeName],
                    multiFSelectors=self.multiFSelectors[outcomeName],
                    sparse=sparse,
                )

            print("[Done. Evaluation:]")
            acc = accuracy_score(ytest, ypred)
            f1 = f1_score(ytest, ypred, average="macro")
            testCounter = Counter(ytest)
            mfclass = Counter(ytest).most_common(1)[0][0]
            mfclass_acc = testCounter[mfclass] / float(len(ytest))
            matt_ccoef = matthews_corrcoef(ytest, ypred)
            precision = precision_score(ytest, ypred, average="macro")
            recall = recall_score(ytest, ypred, average="macro")
            conf_matrix = confusion_matrix(ytest, ypred)
            # tn, fp, fn, tp = conf_matrix.ravel()
            # specificity = tn / (tn+fp)

            print(" *confusion matrix: \n%s" % str(conf_matrix))
            print(" *precision and recall: \n%s" % classification_report(ytest, ypred))
            print(" *ACC: %.4f (mfclass_acc: %.4f); mfclass: %s" % (acc, mfclass_acc, str(mfclass)))

            classes = list(set(ytest))
            multiclass = True if len(classes) > 2 else False
            if probs:
                auc = computeAUC(ytest, ypredProbs, multiclass, negatives=False, classes=classes)
                print(" *AUC: %.4f" % auc)

            print(" *f1 (macro): %.4f " % (f1))
            print(" *matt_ccoef: %.4f " % (matt_ccoef))
            print(" *precision: %.4f " % (precision))
            print(" *recall: %.4f " % (recall))
            if not multiclass:
                recall_sensitivity = recall_score(ytest, ypred, average='macro')
                recall_specificity = recall_score(np.abs(np.array(ytest) - 1), np.abs(np.array(ypred)-1), average='macro')
                print("  *sensitivity: %.4f (at default class split)" % (recall_sensitivity))
                print("  *specificity: %.4f (at default class split)" % (recall_specificity))
            # print(" *specificity: %.4f " % (specificity))

            mse = metrics.mean_squared_error(ytest, ypred)
            print("*Mean Squared Error:                 %.4f" % mse)
            assert len(thisTestGroupsOrder) == len(ypred), "can't line predictions up with groups"
            if probs:
                predictions[outcomeName] = dict(list(zip(thisTestGroupsOrder, ypredProbsMaxClass)))
            else:
                predictions[outcomeName] = dict(list(zip(thisTestGroupsOrder, ypred)))

            if self.trainBootstrapNames and outcomeName in self.trainBootstrapNames:
                print("\n Bootstrapped Models Found; Evaluating...")
                resultsPerN = {}
                for n, modelNames in self.trainBootstrapNames[outcomeName].items():
                    currentResults = []
                    for bsModelName in modelNames:
                        print("   [running %s]" % bsModelName)
                        ypredProbs, ypredClasses = self._multiXpredict(
                            self.classificationModels[bsModelName],
                            multiXtest,
                            multiScalers=self.multiScalers[bsModelName],
                            multiFSelectors=self.multiFSelectors[bsModelName],
                            sparse=sparse,
                            probs=True,
                        )
                        ypred = ypredClasses[ypredProbs.argmax(axis=1)]
                        currentResults.append(self.classificationMetrics(ytest, ypred, ypredProbs))
                    resultsPerN[n] = self.averageMetrics(currentResults)
                print(" [Done. Results:]")
                pprint(resultsPerN)

        print("\n[Prediction Complete]")

        return predictions

    def averageMetrics(self, results):
        resultsD = {k: [dic[k] for dic in results] for k in results[0]}
        meanSDs = {}
        for metric, data in resultsD.items():
            meanSDs[metric] = (np.mean(data), np.std(data))
        return meanSDs

    def classificationMetrics(self, ytest, ypred, ypredProbs=None):
        testCounter = Counter(ytest)
        mfclass = Counter(ytest).most_common(1)[0][0]
        mfclass_acc = testCounter[mfclass] / float(len(ytest))
        classes = list(set(ytest))
        multiclass = True if len(classes) > 2 else False
        auc = 0.0
        if isinstance(ypredProbs, np.ndarray):
            auc = computeAUC(ytest, ypredProbs, multiclass, negatives=False, classes=classes)
        return {
            "auc": auc,
            "acc": accuracy_score(ytest, ypred),
            "mfc_acc": mfclass_acc,
            "f1": f1_score(ytest, ypred, average="macro"),
            "precision": precision_score(ytest, ypred, average="macro"),
            "recall": recall_score(ytest, ypred, average="macro"),
            "matt_ccoef": matthews_corrcoef(ytest, ypred),
        }

    def predictNoOutcomeGetter(self, groups, standardize=True, sparse=False, restrictToGroups=None):

        outcomes = list(self.classificationModels.keys())

        ####################
        # 2. get data for Xs:
        groupNormsList = []
        XGroups = None  # holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        UGroups = None
        for i in range(len(self.featureGetters)):
            fg = self.featureGetters[i]
            (groupNorms, newFeatureNames) = fg.getGroupNormsSparseFeatsFirst(groups)

            print(" [Aligning current X with training X: feature group: %d]" % i)
            groupNormValues = []

            for feat in self.featureNamesList[i]:
                # groupNormValues is a list in order of featureNamesList of all the group_norms
                groupNormValues.append(groupNorms.get(feat, {}))

            groupNormsList.append(groupNormValues)
            print("  Features Aligned: %d" % len(groupNormValues))

            fgGroups = getGroupsFromGroupNormValues(groupNormValues)
            # fgGroups has diff nb cause it's a chunk

            if not XGroups:
                XGroups = set(fgGroups)
                UGroups = set(fgGroups)
            else:
                XGroups = XGroups & fgGroups  # intersect groups from all feature tables
                UGroups = UGroups | fgGroups  # intersect groups from all feature tables
                # potential source of bug: if a sparse feature table doesn't have all the groups it should
                # potential source of bug: if a sparse feature table doesn't have all of the groups which it should
        # XGroups = XGroups & groups #this should not be needed
        if len(XGroups) < len(groups):
            print(
                " Different number of groups available for different outcomes. (%d, %d)"
                % (len(XGroups), len(groups))
            )

        #########################################
        # 3. predict for all possible outcomes
        predictions = dict()
        # testGroupsOrder = list(UGroups)
        testGroupsOrder = list(XGroups)

        for outcomeName in sorted(outcomes):
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            thisTestGroupsOrder = testGroupsOrder

            multiXtest = []
            for i in range(len(groupNormsList)):  # get each feature group data (i.e. feature table)

                groupNormValues = groupNormsList[i]  # basically a feature table in list(dict) form
                # We want the dictionaries to turn into a list that is aligned
                gns = dict(list(zip(self.featureNamesList[i], groupNormValues)))
                # print "Maarten", str(gns)[:150]
                df = pd.DataFrame(data=gns)
                df = df.fillna(0.0)
                df = df[self.featureNamesList[i]]
                df = df.reindex(thisTestGroupsOrder)
                print("  (feature group: %d)" % (i))

                multiXtest.append(csr_array(df.values))

                # print "Maarten", csr_matrix(df.values).shape, csr_matrix(df.values).todense()

            #############
            # 4) predict
            ypred = self._multiXpredict(
                self.classificationModels[outcomeName],
                multiXtest,
                multiScalers=self.multiScalers[outcomeName],
                multiFSelectors=self.multiFSelectors[outcomeName],
                sparse=sparse,
            )
            print("[Done.]")

            assert len(thisTestGroupsOrder) == len(ypred), "can't line predictions up with groups"
            predictions[outcomeName] = dict(list(zip(thisTestGroupsOrder, ypred)))

        print("[Prediction Complete]")

        return predictions

    def predictAllToFeatureTable(
        self, standardize=True, sparse=False, fe=None, name=None, groupsWhere=""
    ):
        if not fe:
            print("Must provide a feature extractor object")
            sys.exit(0)

        # handle large amount of predictions:
        (groups, allOutcomes, controls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )

        if len(allOutcomes) == 0:
            print(
                """
      ERROR: predictToFeatureTable doesn't work when --outcome_table
             and --outcomes are not specified, please make a dummy
             table containing zero-ed outcome columns
             """
            )
            sys.exit(0)

        groups = list(groups)
        # groups contains all groups that are in the outcome table and that have outcome values not null

        chunks = [groups]
        # split groups into chunks
        if len(groups) > self.maxPredictAtTime:
            random.seed(self.randomState)
            random.shuffle(groups)
            chunks = [x for x in foldN(groups, int(ceil(len(groups) / self.maxPredictAtTime)))]
        predictions = dict()
        totalPred = 0

        featNames = None
        featLength = None
        featureTableName = ""

        for chunk in chunks:
            if len(chunk) == len(groups):
                print("len(chunk) == len(groups): True")
                # chunk = None

            chunkPredictions = self.predict(standardize, sparse, chunk)

            # predictions is now outcomeName => group_id => value (outcomeName can become feat)
            # merge chunk predictions into predictions:
            for outcomeName in chunkPredictions.keys():
                try:
                    predictions[outcomeName].update(chunkPredictions[outcomeName])
                except KeyError:
                    predictions[outcomeName] = chunkPredictions[outcomeName]
            totalPred += len(chunk)
            print(" Total Predicted: %d" % totalPred)

            # INSERTING the chunk into MySQL
            # Creating table if not done yet
            if not featNames:
                featNames = list(chunkPredictions.keys())
                featLength = max([len(s) for s in featNames])
                # CREATE TABLE, and insert into it progressively:
                featureName = "p_%s" % self.modelName[:4]
                if name:
                    featureName += "_" + name
                featureTableName = fe.createFeatureTable(
                    featureName, "VARCHAR(%d)" % featLength, "DOUBLE"
                )

            written = 0
            rows = []
            for feat in featNames:
                preds = chunkPredictions[feat]
                # pprint(preds)#DEBUG
                print("[Inserting Predictions as Feature values for feature: %s]" % feat)
                wsql = """INSERT INTO """+featureTableName+""" (group_id, feat, value, group_norm) values (%s, '"""+feat+"""', %s, %s)"""
                wCursor = mm.dbConnect(self.corpdb, host=self.mysql_host, charset=self.encoding, use_unicode=self.use_unicode, mysql_config_file=self.mysql_config_file)[1]
                
                for k, v in preds.items():
                    rows.append((k, v, v))
                    if len(rows) >  self.maxPredictAtTime or len(rows) >= len(preds):
                        mm.executeWriteMany(fe.corpdb, fe.dbCursor, wsql, rows, writeCursor=wCursor, charset=fe.encoding, use_unicode=fe.use_unicode, mysql_config_file=fe.mysql_config_file)
                        written += len(rows)
                        print("   %d feature rows written" % written)
                        rows = []
            # if there's rows left
            if rows:
                wCursor = mm.dbConnect(self.corpdb, host=self.mysql_host, charset=self.encoding, use_unicode=self.use_unicode, mysql_config_file=self.mysql_config_file)[1]
                mm.executeWriteMany(fe.corpdb, fe.dbCursor, wsql, rows, writeCursor=wCursor, charset=fe.encoding, use_unicode=fe.use_unicode, mysql_config_file=fe.mysql_config_file)
                written += len(rows)
                print("   %d feature rows written" % written)
        return

    def predictToOutcomeTable(
        self,
        standardize=True,
        sparse=False,
        fe=None,
        name=None,
        restrictToGroups=None,
        groupsWhere="",
    ):

        # if not self.multiXOn:
        #     print("model trained without multiX, reverting to old predict")
        #     return self.old_predict(standardize, sparse, restrictToGroups)

        # ################
        # #1. setup groups
        # (groups, allOutcomes, allControls) = self.outcomeGetter.getGroupsAndOutcomes(groupsWhere = groupsWhere)
        # if restrictToGroups: #restrict to groups
        #     rGroups = restrictToGroups
        #     if isinstance(restrictToGroups, dict):
        #         rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
        #     groups = groups.intersection(rGroups)
        #     for outcomeName, outcomes in allOutcomes.items():
        #         allOutcomes[outcomeName] = dict([(g, outcomes[g]) for g in groups if (g in outcomes)])
        #     for controlName, controlValues in allControls.items():
        #         controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        # print("[number of groups: %d]" % (len(groups)))

        # ####################
        # #2. get data for Xs:
        # groupNormsList = []
        # XGroups = None #holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        # UGroups = None
        # for i in range(len(self.featureGetters)):
        #     fg = self.featureGetters[i]
        #     (groupNorms, newFeatureNames) = fg.getGroupNormsSparseFeatsFirst(groups)

        #     print(" [Aligning current X with training X: feature group: %d]" %i)
        #     groupNormValues = []
        #     #print self.featureNamesList[i][:10]#debug
        #     for feat in self.featureNamesList[i]:
        #         if feat in groupNorms:
        #             groupNormValues.append(groupNorms[feat])
        #         else:
        #             groupNormValues.append(dict())
        #     groupNormsList.append(groupNormValues)
        #     print("  Features Aligned: %d" % len(groupNormValues))
        #     fgGroups = getGroupsFromGroupNormValues(groupNormValues)
        #     if not XGroups:
        #         XGroups = set(fgGroups)
        #         UGroups = set(fgGroups)
        #     else:
        #         XGroups = XGroups & fgGroups #intersect groups from all feature tables
        #         UGroups = UGroups | fgGroups #intersect groups from all feature tables
        #         #potential source of bug: if a sparse feature table doesn't have all the groups it should
        #         #potential source of bug: if a sparse feature table doesn't have all of the groups which it should
        # #XGroups = XGroups & groups #this should not be needed
        # if len(XGroups) < len(groups):
        #     print(" Different number of groups available for different outcomes.")

        # ################################
        # #2b) setup control data:
        # controlValues = list(allControls.values())
        # if controlValues:
        #     groupNormsList.append(controlValues)

        # #########################################
        # #3. predict for all possible outcomes
        # predictions = dict()
        # testGroupsOrder = list(UGroups)
        # #testGroupsOrder = list(XGroups)
        # for outcomeName, outcomes in sorted(allOutcomes.items()):
        #     print("\n= %s =\n%s"%(outcomeName, '-'*(len(outcomeName)+4)))
        #     if isinstance(restrictToGroups, dict): #outcome specific restrictions:
        #         outcomes = dict([(g, o) for g, o in outcomes.items() if g in restrictToGroups[outcomeName]])
        #     thisTestGroupsOrder = [gid for gid in testGroupsOrder if gid in outcomes]
        #     if len(thisTestGroupsOrder) < len(testGroupsOrder):
        #         print("   this outcome has less groups. Shrunk groups to %d total." % (len(thisTestGroupsOrder)))
        #     (multiXtest, ytest) = ([], None)
        #     for i in range(len(groupNormsList)): #get each feature group data (i.e. feature table)
        #         groupNormValues = groupNormsList[i]
        #         (Xdicts, ydict) = (groupNormValues, outcomes)
        #         print("  (feature group: %d)" % (i))
        #         (Xtest, ytest) = alignDictsAsXy(Xdicts, ydict, sparse=True, keys = thisTestGroupsOrder)
        #         multiXtest.append(Xtest)

        #         print("   [Test size: %d ]" % (len(ytest)))

        #     #############
        #     #4) predict
        #     ypred = self._multiXpredict(self.classificationModels[outcomeName], multiXtest, multiScalers = self.multiScalers[outcomeName], \
        #                                     multiFSelectors = self.multiFSelectors[outcomeName], sparse = sparse)
        #     print("[Done. Evaluation:]")
        #     acc = accuracy_score(ytest, ypred)
        #     f1 = f1_score(ytest, ypred)
        #     testCounter = Counter(ytest)
        #     mfclass = Counter(ytest).most_common(1)[0][0]
        #     mfclass_acc = testCounter[mfclass] / float(len(ytest))
        #     print(" *confusion matrix: \n%s"% str(confusion_matrix(ytest, ypred)))
        #     print(" *precision and recall: \n%s" % classification_report(ytest, ypred))
        #     print(" *ACC: %.4f (mfclass_acc: %.4f); mfclass: %s\n" % (acc, mfclass_acc, str(mfclass)))

        #     mse = metrics.mean_squared_error(ytest, ypred)
        #     print("*Mean Squared Error:                 %.4f"% mse)
        #     assert len(thisTestGroupsOrder) == len(ypred), "can't line predictions up with groups"
        #     predictions[outcomeName] = dict(list(zip(thisTestGroupsOrder,ypred)))

        # print("[Prediction Complete]")

        # #featNames = list(predictions.keys())
        # predDF = pd.DataFrame(predictions)
        # # print predDF

        # name = "p_%s" % self.modelName[:4] + "$" + name
        # # 4: use self.outcomeGetter.createOutcomeTable(tableName, dataFrame)
        # self.outcomeGetter.createOutcomeTable(name, predDF, 'replace')

        # step1: get groups from feature table
        groups = self.featureGetter.getDistinctGroupsFromFeatTable()
        groups = list(groups)
        chunks = [groups]

        # 2: chunks of groups (only if necessary)
        if len(groups) > self.maxPredictAtTime:
            numChunks = int(len(groups) / float(self.maxPredictAtTime)) + 1
            print(
                "TOTAL GROUPS (%d) TOO LARGE. Breaking up to run in %d chunks."
                % (len(groups), numChunks)
            )
            random.seed(self.randomState)
            random.shuffle(groups)
            chunks = [x for x in foldN(groups, numChunks)]

        predictions = dict()  # outcomes->groups->prediction

        totalPred = 0
        for c, chunk in enumerate(chunks):
            print("\n\n**CHUNK %d\n" % c)

            # 3: predict for each chunk for each outcome

            chunkPredictions = self.predictNoOutcomeGetter(chunk, standardize, sparse)
            # predictions is now outcomeName => group_id => value (outcomeName can become feat)
            # merge chunk predictions into predictions:
            for outcomeName in chunkPredictions.keys():
                try:
                    predictions[outcomeName].update(chunkPredictions[outcomeName])
                except KeyError:
                    predictions[outcomeName] = chunkPredictions[outcomeName]
            if chunk:
                totalPred += len(chunk)
            else:
                totalPred = len(groups)
            print(" Total Predicted: %d" % totalPred)

        featNames = list(predictions.keys())
        predDF = pd.DataFrame(predictions)
        # print predDF

        name = "p_%s" % self.modelName[:4] + "$" + name
        # 4: use self.outcomeGetter.createOutcomeTable(tableName, dataFrame)
        self.outcomeGetter.createOutcomeTable(name, predDF, "replace")

    def predictToFeatureTable(
        self, standardize=True, sparse=False, fe=None, name=None, groupsWhere="", probs=False
    ):
        if not fe:
            print("Must provide a feature extractor object")
            sys.exit(0)

        # handle large amount of predictions:
        (groups, allOutcomes, controls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )

        if len(allOutcomes) == 0:
            print(
                """
      ERROR: predictToFeatureTable doesn't work when --outcome_table
             and --outcomes are not specified, please make a dummy
             table containing zero-ed outcome columns
             """
            )
            sys.exit(0)

        groups = list(groups)
        # groups contains all groups that are in the outcome table and that have outcome values not null

        chunks = [groups]
        # split groups into chunks
        if len(groups) > self.maxPredictAtTime:
            random.seed(self.randomState)
            random.shuffle(groups)
            chunks = [x for x in foldN(groups, int(ceil(len(groups) / self.maxPredictAtTime)))]
        predictions = dict()
        totalPred = 0

        featNames = None
        featLength = None
        featureTableName = ""

        for chunk in chunks:
            if len(chunk) == len(groups):
                print("len(chunk) == len(groups): True")
                # chunk = None

            chunkPredictions = self.predict(standardize, sparse, chunk, probs=probs)

            # predictions is now outcomeName => group_id => value (outcomeName can become feat)
            # merge chunk predictions into predictions:
            for outcomeName in chunkPredictions.keys():
                try:
                    predictions[outcomeName].update(chunkPredictions[outcomeName])
                except KeyError:
                    predictions[outcomeName] = chunkPredictions[outcomeName]
            totalPred += len(chunk)
            print(" Total Predicted: %d" % totalPred)

            # INSERTING the chunk into MySQL
            # Creating table if not done yet
            if not featNames:
                featNames = list(chunkPredictions.keys())
                featLength = max([len(s) for s in featNames])
                # CREATE TABLE, and insert into it progressively:
                featureName = "p_%s" % self.modelName[:4]
                if name:
                    featureName += "_" + name
                featureTableName = fe.createFeatureTable(
                    featureName, "VARCHAR(%d)" % featLength, "DOUBLE"
                )

            written = 0
            rows = []
            for feat in featNames:
                preds = chunkPredictions[feat]
                # pprint(preds)#DEBUG
                print("[Inserting Predictions as Feature values for feature: %s]" % feat)
                #wsql = """INSERT INTO """+featureTableName+""" (group_id, feat, value, group_norm) values (%s, '"""+feat+"""', %s, %s)"""
                query = fe.qb.create_insert_query(featureTableName).set_values([("group_id",""),("feat",feat),("value",""),("group_norm","")])
                
                for k, v in preds.items():
                    rows.append((k, float(v), float(v)))
                    if len(rows) >  self.maxPredictAtTime or len(rows) >= len(preds):
                        query.execute_query(rows)
                        #mm.executeWriteMany(fe.corpdb, fe.dbCursor, wsql, rows, writeCursor=fe.dbConn.cursor(), charset=fe.encoding, use_unicode=fe.use_unicode, mysql_config_file=fe.mysql_config_file)
                        written += len(rows)
                        print("   %d feature rows written" % written)
                        rows = []
            # if there's rows left
            if rows:
                query.execute_query(rows)
                #mm.executeWriteMany(fe.corpdb, fe.dbCursor, wsql, rows, writeCursor=fe.dbConn.cursor(), charset=fe.encoding, use_unicode=fe.use_unicode, mysql_config_file=fe.mysql_config_file)
                written += len(rows)
                print("   %d feature rows written" % written)
        return

    def getWeightsForFeaturesAsADict(self):
        """Creates a lexicon from a topic file

        Returns
        -------
        weights_dict : dict
            dictionary of featureTable -> outcomes -> feature_name -> weight
        """

        weights_dict = dict()
        unpackTopicWeights = dict()
        intercept_dict = dict()
        featTables = [fg.featureTable for fg in self.featureGetters]
        for i, featTableFeats in enumerate(self.featureNamesList):
            if "cat_" in featTables[i]:
                unpackTopicWeights[i] = featTables[i]

            weights_dict[featTables[i]] = dict()
            for outcome, model in self.classificationModels.items():
                coefficients = eval(
                    "self.classificationModels[outcome].%s"
                    % self.modelToCoeffsName[self.modelName.lower()]
                )
                if np.all(coefficients == 0):
                    warn("WARNING: All coefficients equal to zero for outcome %s" % outcome)
                    continue
                weights_dict[featTables[i]][outcome] = dict()

                coeff_iter = iter(coefficients.flatten())
                coefficients = np.asarray(
                    [list(islice(coeff_iter, 0, j)) for j in self.featureLengthDict[outcome]][i]
                )

                # Inverting Feature Selection
                if self.multiFSelectors[outcome][i]:
                    print("Inverting the feature selection: %s" % self.multiFSelectors[outcome][i])
                    coefficients = (
                        self.multiFSelectors[outcome][i].inverse_transform(coefficients).flatten()
                    )

                # Inverting Feature Selection
                scaler_intercept = 0
                if self.multiScalers[outcome][i]:
                    print("Inverting the scaling: %s" % self.multiScalers[outcome][i])
                    if self.multiScalers[outcome][i].mean_ is not None:
                        means = self.multiScalers[outcome][i].mean_
                    else:
                        means = [0 for ii, coeff in enumerate(coefficients)]
                    if self.multiScalers[outcome][i].scale_ is not None:
                        scales = self.multiScalers[outcome][i].scale_
                    else:
                        scales = [1 for ii, coeff in enumerate(coefficients)]
                    scaler_intercept = sum(
                        [coeff * means[ii] / scales[ii] for ii, coeff in enumerate(coefficients)]
                    )
                    coefficients = np.asarray(
                        [coeff / scales[ii] for ii, coeff in enumerate(coefficients)]
                    )

                if "mean_" in dir(self.multiFSelectors[outcome][i]):
                    print("RPCA mean: ", self.multiFSelectors[outcome][i].mean_)

                # featTableFeats contains the list of features
                if len(coefficients) != len(featTableFeats):
                    print(
                        "length of coefficients (%d) does not match number of features (%d)"
                        % (len(coefficients), len(featTableFeats))
                    )
                    sys.exit(1)

                intercept = self.classificationModels[outcome].intercept_
                if outcome not in intercept_dict:
                    intercept_dict[outcome] = intercept - scaler_intercept
                    print("Intercept for {o} [{i}]".format(o=outcome, i=intercept_dict[outcome]))
                print(
                    "coefficients size for {f}: {s}".format(f=featTables[i], s=coefficients.shape)
                )
                coefficients.resize(1, len(coefficients))
                coefficients = coefficients.flatten()

                weights_dict[featTables[i]][outcome] = {
                    featTableFeats[j]: coefficients[j]
                    for j in range(len(featTableFeats))
                    if coefficients[j] != 0
                }

        if unpackTopicWeights:
            # only topic tables
            if len(unpackTopicWeights) == len(weights_dict):
                # single topic table
                if len(unpackTopicWeights) == 1:
                    topicFeatTable = unpackTopicWeights[list(unpackTopicWeights)[0]]
                    print("Unpacking {topicFeatTable}".format(topicFeatTable=topicFeatTable))
                    weights_dict, buildTable = self.unpackTopicTables(
                        self.featureGetters[0], topicFeatTable, weights_dict
                    )
                # multiple topic tables
                else:
                    weights_dict["words"] = dict()
                    first = True
                    for idx, topicFeatTable in unpackTopicWeights.items():
                        if first:
                            weights_dict["words"] = {
                                o: dict() for o in weights_dict[topicFeatTable].keys()
                            }
                            first = False
                        print("Unpacking {topicFeatTable}".format(topicFeatTable=topicFeatTable))
                        weights_dict, buildTable = self.unpackTopicTables(
                            self.featureGetters[idx], topicFeatTable, weights_dict
                        )
                        for outcome, wordDict in weights_dict[topicFeatTable].items():
                            for word, weight in wordDict.items():
                                if word in weights_dict["words"][outcome]:
                                    weights_dict["words"][outcome][word] += weight
                                else:
                                    weights_dict["words"][outcome][word] = weight
                        print("Combining %s with %s." % (topicFeatTable, '"words"'))
                        del weights_dict[topicFeatTable]

            # mixed tables
            else:
                for idx, topicFeatTable in unpackTopicWeights.items():
                    print("Unpacking {topicFeatTable}".format(topicFeatTable=topicFeatTable))
                    weights_dict, buildTable = self.unpackTopicTables(
                        self.featureGetters[idx], topicFeatTable, weights_dict
                    )
                    for featTable in weights_dict:
                        if featTable.split("$")[1].startswith(buildTable):
                            for outcome, wordDict in weights_dict[topicFeatTable].items():
                                for word, weight in wordDict.items():
                                    if word in weights_dict[featTable][outcome]:
                                        weights_dict[featTable][outcome][word] += weight
                                    else:
                                        weights_dict[featTable][outcome][word] = weight
                            print("Combining %s with %s." % (topicFeatTable, featTable))
                            del weights_dict[topicFeatTable]
                            break

        # add in intercepts
        for featTable in weights_dict:
            for outcome in weights_dict[featTable]:
                weights_dict[featTable][outcome]["_intercept"] = intercept_dict[outcome]
        return weights_dict

    def unpackTopicTables(self, featureGetter, topicFeatTable, weightsDict):
        """Convert topics coefficients to single words with coefficients*topic_word_probabilities

        Parameters
        ----------
        featureGetter : obj

        topicFeatTable : str
            New (topic) lexicon name.
        weights_dict : dict
            dictionary of featureTable -> outcomes -> feature_name -> weight

        Returns
        -------
        weights_dict : dict
            updated dictionary of featureTable -> outcomes -> feature_name -> weight

        buildTable : str
            Abbriviation of word table used for topic extraction
        """

        try:
            _, topicTable, msgTable, correlField, transform = topicFeatTable.split("$")
            topicTable = topicTable.replace("cat_", "").replace("_w", "")
        except:
            print("Nonstandard feature table name: {f}".format(f=topicFeatTable))
            sys.exit(1)

        buildTable = "1gram"
        if "16to" not in transform:
            buildTable = transform

        lex_dict = dict()
        sql = """SELECT term, category, weight from {lexDB}.{lexTable}""".format(lexDB=featureGetter.lexicondb, lexTable=topicTable)
        rows = mm.executeGetList(featureGetter.corpdb, featureGetter.dbCursor, sql, charset=featureGetter.encoding, use_unicode=featureGetter.use_unicode, mysql_config_file=featureGetter.mysql_config_file)
        for row in rows:
            term, category, weight = str(row[0]).strip(), str(row[1]).strip(), float(row[2])
            if term not in lex_dict:
                lex_dict[term] = dict()
            lex_dict[term][category] = weight

        for outcome in weightsDict[topicFeatTable]:
            summedWordWeights = dict()
            for term in lex_dict:
                this_sum = 0
                for category in lex_dict[term]:
                    if category in weightsDict[topicFeatTable][outcome]:
                        this_sum += (
                            weightsDict[topicFeatTable][outcome][category]
                            * lex_dict[term][category]
                        )
                summedWordWeights[term] = this_sum
            weightsDict[topicFeatTable][outcome] = summedWordWeights

        return weightsDict, buildTable

    def _train(self, X, y, standardize=True):
        """does the actual classification training, first feature selection: can be used by both train and test"""

        sparse = True
        if not isinstance(X, csr_array):
            X = np.array(X)
            sparse = False

        scaler = None
        # print " Standardize: ", standardize
        if standardize == True:
            scaler = StandardScaler(with_mean=not sparse)
            print("[Applying StandardScaler to X: %s]" % str(scaler))
            X = scaler.fit_transform(X)
        y = np.array(y)
        print(" (N, features): %s" % str(X.shape))

        fSelector = None
        if self.featureSelectionString and X.shape[1] >= self.featureSelectMin:
            fSelector = eval(self.featureSelectionString)
            if self.featureSelectPerc < 1.0:
                print(
                    "[Applying Feature Selection to %d perc of X: %s]"
                    % (int(self.featureSelectPerc * 100), str(fSelector))
                )
                _, Xsub, _, ysub = train_test_split(
                    X, y, test_size=self.featureSelectPerc, train_size=1, random_state=0
                )
                fSelector.fit(Xsub, ysub)
                newX = fSelector.transform(X)
                if newX.shape[1]:
                    X = newX
                else:
                    print("No features selected, so using original full X")
            else:
                print("[Applying Feature Selection to X: %s]" % str(fSelector))
                newX = fSelector.fit_transform(X, y)
                if newX.shape[1]:
                    X = newX
                else:
                    print("No features selected, so using original full X")
            print(" after feature selection: (N, features): %s" % str(X.shape))
        modelName = self.modelName.lower()
        if (X.shape[1] / float(X.shape[0])) < self.backOffPerc and modelName != self.backOffModel.lower(): #backoff to simpler model:
            print("number of features is small enough, backing off to %s" % self.backOffModel)
            modelName = self.backOffModel.lower()

        if hasMultValuesPerItem(self.cvParams[modelName]) and modelName[-2:] != "cv":

            # grid search for classifier params:
            gs = GridSearchCV(
                eval(self.modelToClassName[modelName] + "()"),
                self.cvParams[modelName],
                n_jobs=self.cvJobs,
                cv=ShuffleSplit(
                    n_splits=self.cvFolds + 1,
                    test_size=1 / float(self.cvFolds),
                    random_state=DEFAULT_RANDOM_SEED,
                ),
            )
            print("[Performing grid search for parameters over training]")
            gs.fit(X, y)

            print("best estimator: %s (score: %.4f)\n" % (gs.best_estimator_, gs.best_score_))
            return gs.best_estimator_, scaler, fSelector
        else:
            # no grid search
            print("[Training classification model: %s]" % modelName)
            classifier = eval(self.modelToClassName[modelName] + "()")
            classifier.set_params(
                **dict(
                    (k, v[0] if isinstance(v, list) else v)
                    for k, v in self.cvParams[modelName][0].items()
                )
            )
            # print dict(self.cvParams[modelName][0])

            classifier.fit(X, y)
            # print "coefs"
            # print classifier.coef_
            print("model: %s " % str(classifier))
            if modelName[-2:] == "cv" and "alphas" in classifier.get_params():
                print("  selected alpha: %f" % classifier.alpha_)
            return classifier, scaler, fSelector

    def _monteCarloResampleMultiXY(self, multiX, y, N=10, sampleN=None):
        """returns monteCarloResampling (i.e. for bootstrapping average and std based on model)"""
        if not isinstance(multiX, (list, tuple)):
            multiX = [multiX]

        from sklearn.utils import resample

        rs = np.random.RandomState(42)
        for i in range(N):
            *newMultiX, newY = resample(*multiX, y, random_state=rs, n_samples=sampleN)
            yield newMultiX, newY

    def _multiXtrain(
        self, X, y, standardize=True, sparse=False, adaptTables=None, adaptColumns=None, classes=[]
    ):
        """does the actual classification training, first feature selection: can be used by both train and test
        create multiple scalers and feature selectors
        and just one classification model (of combining the Xes into 1)
        adapt tables: specifies which table (i.e. index of X) to adapt
        adapt cols: specifies which columns of the last table (X) to use for adapting the adaptTables
        """

        if not isinstance(X, (list, tuple)):
            X = [X]
        multiX = X
        X = None  # to avoid errors
        multiScalers = []
        multiFSelectors = []

        adaptMatrix = np.array([])
        if adaptTables is not None:
            # Youngseo
            print(("MultiX before duplication:", len(multiX)))
            # if adaptCol is empty, it means all columns of the controls table will be used for adaptation.
            controls_mat = multiX[-1].todense()
            if adaptColumns is None:
                adaptMatrix = controls_mat
            else:
                for adaptCol in adaptColumns:
                    # c =np.insert(c,c.shape[1],thelist[0][:,0],axis=1)
                    adaptMatrix = np.insert(
                        adaptMatrix, adaptMatrix.shape[1], controls_mat[:, adaptCol], axis=1
                    )

        try:
            self.featureLengthDict[self.outcomeNames[-1]] = list()
        except Exception as e:
            # probably running cross validation, this information is not needed
            pass

        # for i in xrange(len(multiX)):
        i = 0
        while i < len(multiX):  # changed to while loop by Youngseo
            X = multiX[i]

            if not sparse and isinstance(X, csr_array):  # edited by Youngseo
                X = X.todense()

            # Standardization:
            scaler = None
            # print " Standardize: ", standardize
            if standardize == True:
                scaler = StandardScaler(with_mean=not sparse)
                print(("[Applying StandardScaler to X[%d]: %s]" % (i, str(scaler))))
                X = scaler.fit_transform(X)
                if self.outliersToMean and not sparse:
                    X[abs(X) > self.outliersToMean] = 0
                    print(
                        "  [Setting outliers (> %d) to mean for X[%d]]" % (self.outliersToMean, i)
                    )
                y = np.array(y)
            elif self.outliersToMean:
                print(" Warning: Outliers to mean is not being run because standardize is off")
            print((" X[%d]: (N, features): %s" % (i, str(X.shape))))

            # Feature Selection
            fSelector = None
            if self.featureSelectionString and X.shape[1] >= self.featureSelectMin:
                fSelector = eval(self.featureSelectionString)
                if self.featureSelectPerc < 1.0:
                    print(
                        (
                            "[Applying Feature Selection to %d perc of X: %s]"
                            % (int(self.featureSelectPerc * 100), str(fSelector))
                        )
                    )
                    _, Xsub, _, ysub = train_test_split(
                        X, y, test_size=self.featureSelectPerc, train_size=1, random_state=0
                    )
                    fSelector.fit(Xsub, ysub)
                    newX = fSelector.transform(X)
                    if newX.shape[1]:
                        X = newX
                    else:
                        print("No features selected, so using original full X")
                else:
                    print(("[Applying Feature Selection to X: %s]" % str(fSelector)))
                    newX = fSelector.fit_transform(X, y)
                    if newX.shape[1]:
                        X = newX
                    else:
                        print("No features selected, so using original full X")
                print((" after feature selection: (N, features): %s" % str(X.shape)))

            # Youngseo
            # adaptation:
            if adaptTables is not None and i in adaptTables:
                # print 'adaptaion matrix:', adaptMatrix
                for j in range(adaptMatrix.shape[1]):
                    adaptColMult = adaptMatrix[:, j]
                    # print adaptColMult
                    adaptX = list()
                    for k in range(X.shape[0]):
                        # print np.array(adaptColMult[k] * X[k,:])[0]
                        # np.vstack([adaptX, np.array(adaptColMult[k] * X[k,:])[0]])
                        adaptX.append(np.array(adaptColMult[k] * X[k, :])[0])
                    # print adaptX
                    # to keep the index of controls table as the last table of multiX
                    multiX.insert(len(multiX) - 1, np.array(adaptX))
                # Youngseo
                print(("MultiX length after duplication:", len(multiX)))

            """
            if adaptTables is not None and i in adaptTables:
                    controlsTable=multiX[len(multiX)-1]
                    # if adaptCol is empty, it means all columns of the controls table will be used for adaptation.
                    if adaptColumns is None:
                        for j in range(adaptMatrix.shape[1]):
                            adaptColMult=adaptMatrix[:,j]
                            
                            print adaptColMult
                            adaptX = X*adaptColMult.reshape((adaptColMult.shape[0],1))
                            # to keep the index of controls table as the last table of multiX
                            multiX.insert(len(multiX)-1,adaptX)
            """

            # if adaptation is set,....
            try:
                self.featureLengthDict[self.outcomeNames[-1]].append(X.shape[1])
            except:
                pass

            multiX[i] = X
            multiScalers.append(scaler)
            multiFSelectors.append(fSelector)
            i += 1  # added to work with while loop by Youngseo Son

        # combine all multiX into one X:
        X = multiX[0]
        if len(classes) > 2:
            y = label_binarize(y, classes=sorted(classes))
        for nextX in multiX[1:]:
            try:
                X = matrixAppendHoriz(X, nextX)
            except ValueError as e:
                print(("ValueError: %s" % str(e)))
                print("couldn't append arrays: perhaps one is sparse and one dense")
                sys.exit(0)
        modelName = self.modelName.lower()
        if (X.shape[1] / float(X.shape[0])) < self.backOffPerc and modelName != self.backOffModel.lower(): #backoff to simpler model:
            print(("number of features is small enough, backing off to %s" % self.backOffModel))
            modelName = self.backOffModel.lower()

        if hasMultValuesPerItem(self.cvParams[modelName]) and modelName[-2:] != "cv":
            # grid search for classifier params:
            if len(classes) > 2:
                parameters = {'estimator__' + k: v for k,v in self.cvParams[modelName][0].items()}
                gs = GridSearchCV(OneVsRestClassifier(eval(self.modelToClassName[modelName]+'()')), 
                                  param_grid=parameters, n_jobs = self.cvJobs,
                                  cv=ShuffleSplit(n_splits=(self.cvFolds+1), test_size=1/float(self.cvFolds), random_state=0))
            else:
                gs = GridSearchCV(
                    eval(self.modelToClassName[modelName] + "()"),
                    self.cvParams[modelName],
                    n_jobs=self.cvJobs,
                    cv=ShuffleSplit(
                        n_splits=self.cvFolds + 1,
                        test_size=1 / float(self.cvFolds),
                        random_state=DEFAULT_RANDOM_SEED,
                    ),
                )
            print("[Performing grid search for parameters over training]")
            gs.fit(X, y)

            print(("best estimator: %s (score: %.4f)\n" % (gs.best_estimator_, gs.best_score_)))
            return gs.best_estimator_, multiScalers, multiFSelectors
        else:
            # no grid search
            print(("[Training classification model: %s]" % modelName))
            classifier = eval(self.modelToClassName[modelName] + "()")
            try:
                classifier.set_params(
                    **dict(
                        (k, v[0] if isinstance(v, list) else v)
                        for k, v in list(self.cvParams[modelName][0].items())
                    )
                )
            except IndexError:
                print("No CV parameters available")
                raise IndexError
            # print dict(self.cvParams[modelName][0])
            if len(classes) > 2:
                classifier = OneVsRestClassifier(classifier)
            try:
                classifier.fit(X, y)
            except ValueError as e:
                print(
                    "ValueError: %s, try using the --no_standardize flag or a different feature selection pipeline"
                    % e
                )
                exit()
            except:
                raise
            # print "coefs"
            # print classifier.coef_
            print(("model: %s " % str(classifier)))
            if modelName[-2:] == "cv" and "alphas" in classifier.get_params():
                print(("  selected alpha: %f" % classifier.alpha_))
            return classifier, multiScalers, multiFSelectors

    def _predict(self, classifier, X, scaler=None, fSelector=None, y=None):
        if scaler:
            X = scaler.transform(X)
        if fSelector:
            newX = fSelector.transform(X)
            if newX.shape[1]:
                X = newX
            else:
                print("No features selected, so using original full X")

        return classifier.predict(X)

    def roc(
        self,
        standardize=True,
        sparse=False,
        restrictToGroups=None,
        output_name=None,
        groupsWhere="",
    ):
        """Tests classifier, by pulling out random testPerc percentage as a test set"""

        ################
        # 1. setup groups
        (groups, allOutcomes, allControls) = self.outcomeGetter.getGroupsAndOutcomes(
            groupsWhere=groupsWhere
        )
        if restrictToGroups:  # restrict to groups
            rGroups = restrictToGroups
            if isinstance(restrictToGroups, dict):
                rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
            groups = groups.intersection(rGroups)
            for outcomeName, outcomes in allOutcomes.items():
                allOutcomes[outcomeName] = dict(
                    [(g, outcomes[g]) for g in groups if (g in outcomes)]
                )
            for controlName, controlValues in controls.items():
                controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        print("[number of groups: %d]" % (len(groups)))

        ####################
        # 2. get data for Xs:
        (groupNormsList, featureNamesList) = ([], [])
        XGroups = None  # holds the set of X groups across all feature spaces and folds (intersect with this to get consistent keys across everything
        UGroups = None
        for fg in self.featureGetters:
            (groupNorms, featureNames) = fg.getGroupNormsSparseFeatsFirst(groups)
            groupNormValues = [
                groupNorms[feat] for feat in featureNames
            ]  # list of dictionaries of group_id => group_norm
            groupNormsList.append(groupNormValues)
            # print featureNames[:10]#debug
            featureNamesList.append(featureNames)
            fgGroups = getGroupsFromGroupNormValues(groupNormValues)
            if not XGroups:
                XGroups = set(fgGroups)
                UGroups = set(fgGroups)
            else:
                XGroups = XGroups & fgGroups  # intersect groups from all feature tables
                UGroups = UGroups | fgGroups  # intersect groups from all feature tables
                # potential source of bug: if a sparse feature table doesn't have all the groups it should

        XGroups = (
            XGroups | groups
        )  # probably unnecessary since groups was given when grabbing features (in which case one could just use groups)
        UGroups = (
            UGroups | groups
        )  # probably unnecessary since groups was given when grabbing features (in which case one could just use groups)

        ################################
        # 2b) setup control data:
        controlValues = list(allControls.values())
        if controlValues:
            groupNormsList.append(controlValues)

        #########################################
        # 3. train for all possible ys:
        self.multiXOn = True
        (self.classificationModels, self.multiScalers, self.multiFSelectors) = (
            dict(),
            dict(),
            dict(),
        )
        for outcomeName, outcomes in sorted(allOutcomes.items()):
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            multiXtrain = list()
            # trainGroupsOrder = list(XGroups & set(outcomes.keys()))
            trainGroupsOrder = list(UGroups & set(outcomes.keys()))
            for i in range(len(groupNormsList)):
                groupNormValues = groupNormsList[i]
                # featureNames = featureNameList[i] #(if needed later, make sure to add controls to this)
                (Xdicts, ydict) = (groupNormValues, outcomes)
                print("  (feature group: %d)" % (i))
                (Xtrain, ytrain) = alignDictsAsXy(Xdicts, ydict, sparse=True, keys=trainGroupsOrder)
                if len(ytrain) > self.trainingSize:
                    Xtrain, Xthrowaway, ytrain, ythrowaway = train_test_split(
                        Xtrain,
                        ytrain,
                        test_size=len(ytrain) - self.trainingSize,
                        random_state=self.randomState,
                    )
                multiXtrain.append(Xtrain)
                print("   [Train size: %d ]" % (len(ytrain)))

            #############
            # 4) fit model
            (
                self.classificationModels[outcomeName],
                self.multiScalers[outcomeName],
                self.multiFSelectors[outcomeName],
            ) = self._roc(multiXtrain, ytrain, standardize, sparse=sparse, output_name=output_name)

        print("\n[TRAINING COMPLETE]\n")
        self.featureNamesList = featureNamesList

    def _roc(self, X, y, standardize=True, sparse=False, output_name=None):

        X = X
        y = label_binarize(y, classes=list(set(y)))

        if not isinstance(X, (list, tuple)):
            X = [X]
        multiX = X
        X = None  # to avoid errors
        multiScalers = []
        multiFSelectors = []

        for i in range(len(multiX)):
            X = multiX[i]
            if not sparse:
                X = X.todense()

            # Standardization:
            scaler = None
            # print " Standardize: ", standardize
            if standardize == True:
                scaler = StandardScaler(with_mean=not sparse)
                print("[Applying StandardScaler to X[%d]: %s]" % (i, str(scaler)))
                X = scaler.fit_transform(X)
                y = np.array(y)
            print(" X[%d]: (N, features): %s" % (i, str(X.shape)))

            # Feature Selection
            fSelector = None
            if self.featureSelectionString and X.shape[1] >= self.featureSelectMin:
                fSelector = eval(self.featureSelectionString)
                if self.featureSelectPerc < 1.0:
                    print(
                        "[Applying Feature Selection to %d perc of X: %s]"
                        % (int(self.featureSelectPerc * 100), str(fSelector))
                    )
                    _, Xsub, _, ysub = train_test_split(
                        X, y, test_size=self.featureSelectPerc, train_size=1, random_state=0
                    )
                    fSelector.fit(Xsub, ysub)
                    newX = fSelector.transform(X)
                    if newX.shape[1]:
                        X = newX
                    else:
                        print("No features selected, so using original full X")
                else:
                    print("[Applying Feature Selection to X: %s]" % str(fSelector))
                    newX = fSelector.fit_transform(X, y)
                    if newX.shape[1]:
                        X = newX
                    else:
                        print("No features selected, so using original full X")
                print(" after feature selection: (N, features): %s" % str(X.shape))

            multiX[i] = X
            multiScalers.append(scaler)
            multiFSelectors.append(fSelector)

        # combine all multiX into one X:
        X = multiX[0]
        for nextX in multiX[1:]:
            try:
                X = matrixAppendHoriz(X, nextX)
            except ValueError as e:
                print("ValueError: %s" % str(e))
                print("couldn't append arrays: perhaps one is sparse and one dense")
                sys.exit(0)
        modelName = self.modelName.lower()
        if (X.shape[1] / float(X.shape[0])) < self.backOffPerc and modelName != self.backOffModel.lower(): #backoff to simpler model:
            print("number of features is small enough, backing off to %s" % self.backOffModel)
            modelName = self.backOffModel.lower()

        # Here is the place to do ROC
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
        y_score = y_test

        ret = None
        if hasMultValuesPerItem(self.cvParams[modelName]) and modelName[-2:] != "cv":
            # multiple Cs or alphas supplied
            # Split into all cases for all classes of y

            for i in range(y_train.shape[1]):
                y_train_slice = y_train[:, i]
                y_test_slice = y_test[:, i]
                # grid search for classifier params:
                gs = GridSearchCV(
                    eval(self.modelToClassName[modelName] + "()"),
                    self.cvParams[modelName],
                    n_jobs=self.cvJobs,
                    cv=ShuffleSplit(
                        n_splits=self.cvFolds + 1,
                        test_size=1 / float(self.cvFolds),
                        random_state=DEFAULT_RANDOM_SEED,
                    ),
                )
                print("[Performing grid search for parameters over training for class: %d]" % i)
                gs.fit(X_train, y_train_slice)
                fitted_model = gs.best_estimator_
                y_score_slice = fitted_model.decision_function(X_test)
                y_score[:, i] = y_score_slice
                print("best estimator: %s (score: %.4f)\n" % (gs.best_estimator_, gs.best_score_))
            ret = (gs.best_estimator_, multiScalers, multiFSelectors)
            print(set(y_score.flatten()))
            print(modelName)
        else:
            print("[ROC - Using classification model: %s]" % modelName)
            classifier = eval(self.modelToClassName[modelName] + "()")
            classifier.set_params(
                **dict(
                    (k, v[0] if isinstance(v, list) else v)
                    for k, v in self.cvParams[modelName][0].items()
                )
            )
            classifier = OneVsRestClassifier(classifier)
            print("[Training classifier]")
            fitted_model = classifier.fit(X_train, y_train)
            print("[Done training]")
            y_score = fitted_model.decision_function(X_test)
            ret = (fitted_model, multiScalers, multiFSelectors)

        self.roc_curves(y_test, y_score, output_name)

        return ret

    """
    # no grid search
    print "[Training classification model: %s]" % modelName
    classifier = eval(self.modelToClassName[modelName]+'()')
    try: 
    classifier.set_params(**dict((k, v[0] if isinstance(v, list) else v) for k,v in self.cvParams[modelName][0].iteritems()))
    except IndexError: 
    print "No CV parameters available"
    raise IndexError
    #print dict(self.cvParams[modelName][0])
    
    classifier.fit(X, y)
    #print "coefs"
    #print classifier.coef_
    print "model: %s " % str(classifier)
    if modelName[-2:] == 'cv' and 'alphas' in classifier.get_params():
    print "  selected alpha: %f" % classifier.alpha_"""

    def roc_curves(self, y_test, y_score, output_name=None):
        output_name = "ROC" if not output_name else output_name
        try:
            pp = PdfPages(output_name + ".pdf" if output_name[-4:] != ".pdf" else output_name)
        except NameError:
            warn("WARNING: matplotlib PdfPages or plt cannot be imported")
            sys.exit(1)

        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        n_classes = y_test.shape[1]
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        print("ROC AUC (area under the curve)", roc_auc)

        # Plot ROC curve
        figure = plt.figure()
        plt.plot(
            fpr["micro"],
            tpr["micro"],
            label="micro-average ROC curve (area = {0:0.2f})" "".format(roc_auc["micro"]),
        )
        for i in range(n_classes):
            plt.plot(
                fpr[i],
                tpr[i],
                label="ROC curve of class {0} (area = {1:0.2f})" "".format(i, roc_auc[i]),
            )

        plt.plot([0, 1], [0, 1], "k--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Some extension of Receiver operating characteristic to multi-class")
        plt.legend(loc="lower right")
        pp.savefig(figure)

        pp.close()

    def _multiXpredict(
        self,
        classifier,
        X,
        multiScalers=None,
        multiFSelectors=None,
        y=None,
        sparse=False,
        probs=False,
        adaptTables=None,
        adaptColumns=None,
    ):
        if not isinstance(X, (list, tuple)):
            X = [X]

        multiX = X
        X = None  # to avoid errors

        adaptMatrix = np.array([])
        if adaptTables is not None:
            # Youngseo
            print(("MultiX length after duplication:", len(multiX)))

            # if adaptCol is empty, it means all columns of the controls table will be used for adaptation.
            controls_mat = multiX[-1].todense()
            if adaptColumns is None:
                adaptMatrix = controls_mat
            else:
                for adaptCol in adaptColumns:
                    # c =np.insert(c,c.shape[1],thelist[0][:,0],axis=1)
                    adaptMatrix = np.insert(
                        adaptMatrix, adaptMatrix.shape[1], controls_mat[:, adaptCol], axis=1
                    )

        # for i in xrange(len(multiX)):
        i = 0
        while i < len(multiX):  # changed to while loop by Youngseo

            # setup X and transformers:
            X = multiX[i]
            if not sparse and isinstance(X, csr_array):  # edited by Youngseo
                X = X.todense()

            (scaler, fSelector) = (None, None)
            if multiScalers:
                scaler = multiScalers[i]
            if multiFSelectors:
                fSelector = multiFSelectors[i]

            # run transformations:
            if scaler:
                print(
                    ("  predict: applying standard scaler to X[%d]: %s" % (i, str(scaler)))
                )  # debug
                try:
                    X = scaler.transform(X)
                    if self.outliersToMean and not sparse:
                        X[abs(X) > self.outliersToMean] = 0
                        print(
                            (
                                "  predict: setting outliers (> %d) to mean for X[%d]"
                                % (self.outliersToMean, i)
                            )
                        )  # debug
                except NotFittedError as e:
                    warn(e)
                    warn("Fitting scaler")
                    X = scaler.fit_transform(X)
                    if outliersToMean and not sparse:
                        X[abs(X) > self.outliersToMean] = 0
                        print(
                            (
                                "  predict: setting outliers (> %d) to mean for X[%d]"
                                % (self.outliersToMean, i)
                            )
                        )  # debug
            elif self.outliersToMean:
                print(" Warning: Outliers to mean is not being run because standardize is off")

            if fSelector:
                print(
                    ("  predict: applying feature selection to X[%d]: %s" % (i, str(fSelector)))
                )  # debug
                newX = fSelector.transform(X)
                if newX.shape[1]:
                    X = newX
                else:
                    print("No features selected, so using original full X")
            # Youngseo
            # adaptation:

            if adaptTables is not None and i in adaptTables:
                for j in range(adaptMatrix.shape[1]):
                    adaptColMult = adaptMatrix[:, j]
                    # print adaptColMult
                    adaptX = list()
                    for k in range(X.shape[0]):
                        # print np.array(adaptColMult[k] * X[k,:])[0]
                        # np.vstack([adaptX, np.array(adaptColMult[k] * X[k,:])[0]])
                        adaptX.append(np.array(adaptColMult[k] * X[k, :])[0])
                    # print adaptX
                    # to keep the index of controls table as the last table of multiX
                    multiX.insert(len(multiX) - 1, np.array(adaptX))
                # Youngseo
                print(("MultiX length after duplication:", len(multiX)))
                """
                #print adaptMatrix
                for j in range(adaptMatrix.shape[1]):
                    adaptColMult=adaptMatrix[:,j]
                    adaptX = X*adaptColMult.reshape((adaptColMult.shape[0],1))
                    # to keep the index of controls table as the last table of multiX
                    multiX.insert(len(multiX)-1,adaptX)
                """
            """
            if adaptTables is not None:
                if i in adaptTables:
                    controlsTable=multiX[len(multiX)-1]
                    # if adaptCol is empty, it means all columns of the controls table will be used for adaptation.
                    if adaptColumns is None:
                        for j in range(controlsTable.shape[1]):
                            adaptColMult=controlsTable[:,j]
                            adaptX = X*adaptColMult.reshape((adaptColMult.shape[0],1))
                            # to keep the index of controls table as the last table of multiX
                            multiX.insert(len(multiX)-1,adaptX)
                    else:
                        for adaptCol in adaptColumns:
                            adaptColMult=controlsTable[:,adaptCol]
                            adaptX = X*adaptColMult.reshape((adaptColMult.shape[0],1))
                            # to keep the index of controls table as the last table of multiX
                            multiX.insert(len(multiX)-1,adaptX)
            """
            multiX[i] = X
            i += 1  # added to work with while loop by Youngseo Son

        # combine all multiX into one X:
        X = multiX[0]
        for nextX in multiX[1:]:
            X = matrixAppendHoriz(X, nextX)

        print(("  predict: combined X shape: %s" % str(X.shape)))  # debug
        if hasattr(classifier, "intercept_"):
            print(("  predict: classifier intercept: %s" % str(classifier.intercept_)))

        if probs:
            try:
                return classifier.predict_proba(X), classifier.classes_
            except AttributeError:
                confs = classifier.decision_function(X)
                if len(classifier.classes_) == 2:
                    confs = array(list(zip([-1 * c for c in confs], confs)))
                # note: may need to convert to probabilities by dividing by max
                return confs, classifier.classes_

        else:
            return classifier.predict(X)

    ###################
    def load(self, filename, pickle2_7=True):
        print("[Loading %s]" % filename)
        with open(filename, "rb") as f:
            if pickle2_7:
                from .dlaWorker import DLAWorker
                from . import occurrenceSelection, pca_mod

                sys.modules["FeatureWorker"] = DLAWorker
                sys.modules["FeatureWorker.occurrenceSelection"] = occurrenceSelection
                sys.modules["FeatureWorker.pca_mod"] = pca_mod
            tmp_dict = pickle.load(f, encoding="latin1")
            f.close()
        try:
            print("Outcomes in loaded model:", list(tmp_dict["classificationModels"].keys()))
        except KeyError:
            if "regressionModels" in tmp_dict:
                warn("You are trying to load a regression model for classification.")
                warn(
                    "Try the classification version of the flag you are using, for example --predict_classifiers_to_feats instead of --predict_regression_to_feats."
                )
            else:
                warn("No classification models found in the pickle.")
            sys.exit()

        tmp_dict["outcomes"] = list(tmp_dict["classificationModels"].keys())
        self.__dict__.update(tmp_dict)

    def save(self, filename):
        print("[Saving %s]" % filename)
        f = open(filename, "wb")
        toDump = {
            "modelName": self.modelName,
            "classificationModels": self.classificationModels,
            "multiScalers": self.multiScalers,
            "scalers": self.scalers,
            "multiFSelectors": self.multiFSelectors,
            "fSelectors": self.fSelectors,
            "featureNames": self.featureNames,
            "featureNamesList": self.featureNamesList,
            "multiXOn": self.multiXOn,
            "trainBootstrapNames": self.trainBootstrapNames,
        }
        pickle.dump(toDump, f, 2)
        f.close()

    ########################
    @staticmethod
    def printComboControlScoresToCSV(
        scores, outputstream=sys.stdout, paramString=None, delimiter="|"
    ):
        """prints scores with all combinations of controls to csv)"""
        if paramString:
            print(paramString + "\n", file=outputstream)
        i = 0
        outcomeKeys = sorted(scores.keys())
        previousColumnNames = []
        for outcomeName in outcomeKeys:

            outcomeScores = scores[outcomeName]
            # setup column and row names:
            controlNames = sorted(
                list(
                    set(
                        [
                            controlName
                            for controlTuple in list(outcomeScores.keys())
                            for controlName in controlTuple
                        ]
                    )
                )
            )
            rowKeys = sorted(list(outcomeScores.keys()), key=lambda k: len(k))
            # scoreNames = sorted(next(iter(outcomeScores[rowKeys[0]].values())).keys(), key=str.lower)
            scoreNames = sorted(
                list(
                    set(
                        name
                        for k in rowKeys
                        for v in outcomeScores[k].values()
                        for name in list(v.keys())
                    )
                ),
                key=str.lower,
            )

            columnNames = (
                ["row_id", "outcome", "model_controls"] + scoreNames + ["w/ lang."] + controlNames
            )

            # csv:
            csvOut = csv.DictWriter(outputstream, fieldnames=columnNames, delimiter=delimiter)
            if set(columnNames) != set(previousColumnNames):
                firstRow = dict([(str(k), str(k)) for k in columnNames])
                csvOut.writerow(firstRow)
                previousColumnNames = columnNames
            for rk in rowKeys:
                for withLang, sc in outcomeScores[rk].items():
                    i += 1
                    rowDict = {
                        "row_id": i,
                        "outcome": outcomeName,
                        "model_controls": str(rk) + str(withLang),
                    }
                    for cn in controlNames:
                        rowDict[cn] = 1 if cn in rk else 0
                    rowDict["w/ lang."] = withLang
                    rowDict.update(
                        {
                            (k, v)
                            for (k, v) in list(sc.items())
                            if ((k != "predictions") and k != "predictionProbs")
                        }
                    )
                    csvOut.writerow(rowDict)

    @staticmethod
    def printComboControlPredictionsToCSV(scores, outputstream, paramString=None, delimiter="|"):
        """prints predictions with all combinations of controls to csv)"""
        predictionData = {}
        data = defaultdict(list)
        columns = ["Id"]
        if paramString:
            print(paramString + "\n", file=outputstream)
        i = 0
        outcomeKeys = sorted(scores.keys())
        previousColumnNames = []
        # get all group ids
        groups = set()
        for outcomeName in scores:
            for rk in scores[outcomeName]:
                for withLang in scores[outcomeName][rk]:
                    groups.update([k for k in scores[outcomeName][rk][withLang]["predictions"]])

        for outcomeName in outcomeKeys:
            outcomeScores = scores[outcomeName]
            controlNames = sorted(
                list(
                    set(
                        [
                            controlName
                            for controlTuple in list(outcomeScores.keys())
                            for controlName in controlTuple
                        ]
                    )
                )
            )
            rowKeys = sorted(list(outcomeScores.keys()), key=lambda k: len(k))
            for rk in rowKeys:
                for withLang, s in outcomeScores[rk].items():
                    i += 1
                    mc = "_".join(rk)
                    if withLang:
                        mc += "_withLanguage"
                    columns.append(outcomeName + "_" + mc)
                    predictionData[str(i) + "_" + outcomeName + "_" + mc] = s["predictions"]
                    for group_id in groups:
                        if group_id in s["predictions"]:
                            data[group_id].append(s["predictions"][group_id])
                        else:
                            data[group_id].append("nan")

        writer = csv.writer(outputstream)
        writer.writerow(columns)
        for k, v in data.items():
            v.insert(0, k)
            writer.writerow(v)

    @staticmethod
    def printComboControlPredictionProbsToCSV(
        scores, outputstream, paramString=None, delimiter="|"
    ):
        """prints predictions with all combinations of controls to csv)"""
        predictionData = {}
        data = defaultdict(list)
        columns = ["Id"]
        if paramString:
            print(paramString + "\n", file=outputstream)
        i = 0
        outcomeKeys = sorted(scores.keys())
        previousColumnNames = []
        # get all group ids
        groups = set()
        for outcomeName in scores:
            for rk in scores[outcomeName]:
                for withLang in scores[outcomeName][rk]:
                    groups.update([k for k in scores[outcomeName][rk][withLang]["predictionProbs"]])

        for i, outcomeName in enumerate(outcomeKeys):
            outcomeScores = scores[outcomeName]
            controlNames = sorted(
                list(
                    set(
                        [
                            controlName
                            for controlTuple in outcomeScores.keys()
                            for controlName in controlTuple
                        ]
                    )
                )
            )
            rowKeys = sorted(outcomeScores.keys(), key=lambda k: len(k))
            for rk in rowKeys:
                for withLang, s in outcomeScores[rk].items():
                    i += 1
                    mc = "_".join(rk)
                    if withLang:
                        mc += "_withLanguage"
                    columns.append(outcomeName + "_" + mc)
                    predictionData[str(i) + "_" + outcomeName + "_" + mc] = s["predictionProbs"]
                    for group_id in groups:
                        if group_id in s["predictionProbs"]:
                            data[group_id].append(s["predictionProbs"][group_id])
                        else:
                            data[group_id].append("nan")

        writer = csv.writer(outputstream)
        writer.writerow(columns)
        for k, v in data.items():
            v.insert(0, k)
            writer.writerow(v)

    #################
    ## Deprecated:
    def old_train(self, standardize=True, sparse=False, restrictToGroups=None):
        """Trains classification models"""
        # if restrictToGroups is a dict than it is an outcome-specific restriction

        print()
        # 1. get data possible ys (outcomes)
        (groups, allOutcomes, controls) = self.outcomeGetter.getGroupsAndOutcomes()
        if restrictToGroups:  # restrict to groups
            rGroups = restrictToGroups
            if isinstance(restrictToGroups, dict):
                rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
            groups = groups.intersection(rGroups)
            for outcomeName, outcomes in allOutcomes.items():
                allOutcomes[outcomeName] = dict(
                    [(g, outcomes[g]) for g in groups if (g in outcomes)]
                )
            for controlName, controlValues in controls.items():
                controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        print("[number of groups: %d]" % len(groups))

        # 2. get data for X:
        (groupNorms, featureNames) = (None, None)
        if len(self.featureGetters) > 1:
            print("WARNING: multiple feature tables passed in rp.train only handles one for now.")
        if sparse:
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsSparseFeatsFirst(groups)
        else:
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsWithZerosFeatsFirst(groups)

        self.featureNames = list(groupNorms.keys())  # holds the order to expect features
        groupNormValues = list(groupNorms.values())  # list of dictionaries of group => group_norm
        controlValues = list(controls.values())  # list of dictionaries of group=>group_norm
        #     this will return a dictionary of dictionaries

        # 3. Create classifiers for each possible y:
        for outcomeName, outcomes in allOutcomes.items():
            if isinstance(restrictToGroups, dict):  # outcome specific restrictions:
                outcomes = dict(
                    [(g, o) for g, o in outcomes.items() if g in restrictToGroups[outcomeName]]
                )
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            print("[Aligning Dicts to get X and y]")
            (X, y) = alignDictsAsXy(groupNormValues + controlValues, outcomes, sparse)
            (
                self.classificationModels[outcomeName],
                self.scalers[outcomeName],
                self.fSelectors[outcomeName],
            ) = self._train(X, y, standardize)

        print("[Done Training All Outcomes]")

    def old_predict(self, standardize=True, sparse=False, restrictToGroups=None):
        # predict works with all sklearn models
        # 1. get data possible ys (outcomes)
        print()
        (groups, allOutcomes, controls) = self.outcomeGetter.getGroupsAndOutcomes()
        if restrictToGroups:  # restrict to groups
            rGroups = restrictToGroups
            if isinstance(restrictToGroups, dict):
                rGroups = [item for sublist in list(restrictToGroups.values()) for item in sublist]
            groups = groups.intersection(rGroups)
            for outcomeName, outcomes in allOutcomes.items():
                allOutcomes[outcomeName] = dict(
                    [(g, outcomes[g]) for g in groups if (g in outcomes)]
                )
            for controlName, controlValues in controls.items():
                controls[controlName] = dict([(g, controlValues[g]) for g in groups])
        print("[number of groups: %d]" % len(groups))

        # 2. get data for X:
        (groupNorms, featureNames) = (None, None)
        if len(self.featureGetters) > 1:
            print("WARNING: multiple feature tables passed in rp.predict only handles one for now.")
        if sparse:
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsSparseFeatsFirst(groups)
        else:
            (groupNorms, featureNames) = self.featureGetter.getGroupNormsWithZerosFeatsFirst(groups)

        # reorder group norms:
        groupNormValues = []
        predictGroups = None
        print("[Aligning current X with training X]")
        for feat in self.featureNames:
            if feat in groupNorms:
                groupNormValues.append(groupNorms[feat])
            else:
                if sparse:  # assumed all zeros
                    groupNormValues.append(dict())
                else:  # need to insert 0s
                    if not predictGroups:
                        predictGroups = list(groupNorms[next(iter(groupNorms.keys()))].keys())
                    groupNormValues.append(dict([(k, 0.0) for k in predictGroups]))
        # groupNormValues = groupNorms.values() #list of dictionaries of group => group_norm
        print("number of features after alignment: %d" % len(groupNormValues))
        controlValues = list(
            controls.values()
        )  # list of dictionaries of group=>group_norm (TODO: including controls for predict might mess things up)
        #     this will return a dictionary of dictionaries

        # 3. Predict ys for each model:
        predictions = dict()  # outcome=>group_id=>value
        for outcomeName, outcomes in allOutcomes.items():
            print("\n= %s =\n%s" % (outcomeName, "-" * (len(outcomeName) + 4)))
            if isinstance(restrictToGroups, dict):  # outcome specific restrictions:
                outcomes = dict(
                    [(g, o) for g, o in outcomes.items() if g in restrictToGroups[outcomeName]]
                )
            (X, ytest, keylist) = alignDictsAsXy(
                groupNormValues + controlValues, outcomes, sparse, returnKeyList=True
            )
            leny = len(ytest)
            print("[Groups to predict: %d]" % leny)
            print(self.scalers.keys())
            print(self.fSelectors.keys())
            (classifier, scaler, fSelector) = (
                self.classificationModels[outcomeName],
                self.scalers[outcomeName],
                self.fSelectors[outcomeName],
            )
            ypred = None
            if self.chunkPredictions:
                ypred = np.array([])  # chunks:
                for subX, suby in chunks(X, ytest, self.maxPredictAtTime):
                    ysubpred = self._predict(classifier, subX, scaler=scaler, fSelector=fSelector)
                    ypred = np.append(ypred, np.array(ysubpred))
                    print("   num predicticed: %d" % len(ypred))
            else:
                ypred = self._predict(classifier, X, scaler=scaler, fSelector=fSelector)
            print("[Done Predicting. Evaluating]")
            R2 = metrics.r2_score(ytest, ypred)
            print("*R^2 (coefficient of determination): %.4f" % R2)
            print("*R (sqrt R^2):                       %.4f" % sqrt(R2))
            print("*Pearson r:                          %.4f (%.5f)" % pearsonr(ytest, ypred))
            print("*Spearman rho:                       %.4f (%.5f)" % spearmanr(ytest, ypred))
            mse = metrics.mean_squared_error(ytest, ypred)
            print("*Mean Squared Error:                 %.4f" % mse)
            predictions[outcomeName] = dict(list(zip(keylist, ypred)))

        return predictions


####################################################################
##
#


#########################
## Module Methods


def chunks(X, y, size):
    """ Yield successive n-sized chunks from X and Y."""
    if not isinstance(X, csr_array):
        assert len(X) == len(y), "chunks: size of X and y don't match"
    size = max(len(y), size)

    for i in range(0, len(y), size):
        yield X[i : i + size], y[i : i + size]


def grouper(folds, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    n = len(l) / folds
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def xFoldN(l, folds):
    """ Yield successive n-sized chunks from l."""
    n = len(l) // folds
    last = len(l) % folds
    i = 0
    for f in range(folds):
        if last > 0:
            yield l[i : i + n + 1]
            last -= 1
            i += n + 1
        else:
            yield l[i : i + n]
            i += n


def foldN(l, folds):
    return [f for f in xFoldN(l, folds)]


def stratifyGroups(groups, outcomes, folds, randomState=DEFAULT_RANDOM_SEED):
    """breaks groups up into folds such that each fold has at most 1 more of a class than other folds """
    random.seed(randomState)
    xGroups = sorted(list(set(groups) & set(outcomes.keys())))
    outcomesByClass = {}
    for g in xGroups:
        try:
            outcomesByClass[outcomes[g]].append(g)
        except KeyError:
            outcomesByClass[outcomes[g]] = [g]

    groupsPerFold = {f: [] for f in range(folds)}
    countPerFold = {f: 0 for f in range(folds)}

    # add groups to folds per class, keeping track of balance
    for c, gs in outcomesByClass.items():
        foldsOrder = [x[0] for x in sorted(list(countPerFold.items()), key=lambda x: (x[1], x[0]))]
        currentGFolds = foldN(gs, folds)
        i = 0
        for f in foldsOrder:
            groupsPerFold[f].extend(currentGFolds[i])
            countPerFold[f] += len(currentGFolds[i])
            i += 1

    # make sure all outcomes aren't together in the groups:
    for gs in list(groupsPerFold.values()):
        random.shuffle(gs)

    return list(groupsPerFold.values())


def hasMultValuesPerItem(listOfD):
    """returns true if the dictionary has a list with more than one element"""
    if len(listOfD) > 1:
        return True
    for d in listOfD:
        for value in d.values():
            if len(value) > 1:
                return True
    return False


def getGroupsFromGroupNormValues(gnvs):
    return set([k for gns in gnvs for k in gns.keys()])


def matrixAppendHoriz(A, B):
    if isinstance(A, sparray) and isinstance(B, sparray):
        return hstack([A, B])
    elif isinstance(A, np.ndarray) and isinstance(B, np.ndarray):
        return np.append(A, B, 1)
    elif isinstance(A, sparray) and isinstance(B, np.ndarray):
        return np.append(A.todense(), B, 1)
    elif isinstance(A, np.ndarray) and isinstance(B, sparray):
        return np.append(A, B.todense(), 1)
    else:
        raise ValueError(
            "matrix append types not supported: %s and %s" % (type(A).__name__, type(B).__name__)
        )


def r2simple(ytrue, ypred):
    y_mean = sum(ytrue) / float(len(ytrue))
    ss_tot = sum((yi - y_mean) ** 2 for yi in ytrue)
    ss_err = sum((yi - fi) ** 2 for yi, fi in zip(ytrue, ypred))
    r2 = 1 - (ss_err / ss_tot)
    return r2


def ensembleNFoldAUCWeight(outcomes, probsListOfDicts, groupFolds):
    """produce average two probability sets (one for each class), weighted by training AUC; return new probs"""
    newProbs = dict()
    for testChunk in [i for i in range(0, len(groupFolds))]:
        trainGroups = set()
        for chunk in groupFolds[:testChunk] + groupFolds[(testChunk + 1) :]:
            trainGroups.update(chunk)
        testGroups = set(groupFolds[testChunk])
        trainGroupsOrder = list(trainGroups)
        testGroupsOrder = list(testGroups)
        (Xtrain, ytrain) = alignDictsAsXy(probsListOfDicts, outcomes, keys=trainGroupsOrder)
        (Xtest, ytest) = alignDictsAsXy(probsListOfDicts, outcomes, keys=testGroupsOrder)
        classes = set(list(ytrain) + list(ytest))
        weights = np.array([0.0] * Xtest.shape[1])
        sumWeights = 0.0
        for c in range(Xtrain.shape[1]):
            # print(c, Xtrain[:,-1,c])#debug
            weights[c] = (
                (
                    max(computeAUC(ytrain, Xtrain[:, c, :], negatives=False, classes=classes), 0.5)
                    - 0.5
                )
                / 0.5
            ) ** 2
            sumWeights += weights[c]
        weights = np.array([weights / sumWeights])
        warn(weights)  # debug
        # ypred_probs = np.dot(Xtest[:,:,-1], weights.T)
        # print(Xtest)#debug
        ypred_probs = np.dot(np.transpose(Xtest, (0, 2, 1)), weights.T)
        ##TODO: change above to :,:,: to handle multiclass;
        warn("   ENSEMBLE FOLD AUC: %.4f" % computeAUC(ytest, ypred_probs[:, :], classes=classes))
        newProbs.update(dict(zip(testGroupsOrder, ypred_probs)))
    # warn(newProbs)#debug
    return newProbs


def easyNFoldAUCWeight(X, y, folds):
    """build logistic regressor given two sets of decision function outputs, return new probs """
    yscores = []
    # X, y = zip(*sorted(zip(X.tolist(), y)))#make sure always in the same order for consistency of results
    # X = zscore(X)
    X = np.array(X)
    y = np.array(y)
    print(X)
    print(y)
    warn(" [NFOLD TRAIN TESTING Easy LR]")
    groups = range(len(y))
    outcomes = dict(zip(groups, y))
    groupFolds = stratifyGroups(groups, outcomes, folds, randomState=DEFAULT_RANDOM_SEED)
    ymap = []
    print(groupFolds)  # debug
    for testgs in groupFolds:
        testgs = np.array(testgs)
        setgs = set(testgs)
        traings = [i for i in groups if i not in setgs]
        ytest = y[testgs]
        Xtest = X[testgs]
        ytrain = y[traings]
        Xtrain = X[traings]

        weights = np.array([0.0] * Xtest.shape[1])
        sumWeights = 0.0
        for c in range(Xtrain.shape[1]):
            weights[c] = ((np.absolute(pos_neg_auc(ytrain, Xtrain[:, c])) - 0.5) / 0.5) ** 2
            sumWeights += weights[c]
        weights = np.array([weights / sumWeights])
        warn(weights)  # debug
        ypred_probs = np.dot(Xtest, weights.T)
        warn("   EASY LR AUC: %.4f" % pos_neg_auc(ytest, ypred_probs[:, -1]))
        yscores.extend(ypred_probs)
        ymap.extend(testgs)
    newyscores = [0] * len(y)
    for i in groups:
        newyscores[ymap[i]] = yscores[i]
    warn(" [Done]")
    warn(" FINAL EASY LR AUC: %.4f" % pos_neg_auc(y, np.array(newyscores)[:, -1]))
    return newyscores


def paired_t_1tail_on_errors(newprobs, oldprobs, ytrue):
    #computes paired t-test on error (not clear if valid for classification)
    n = len(ytrue)
    newprobs_res_abs = np.absolute(array(ytrue) - array(newprobs))
    oldprobs_res_abs = np.absolute(array(ytrue) - array(oldprobs))
    ypp_diff = newprobs_res_abs - oldprobs_res_abs  # old should be smaller
    ypp_diff_mean, ypp_sd = np.mean(ypp_diff), np.std(ypp_diff)
    ypp_diff_t = ypp_diff_mean / (ypp_sd / sqrt(n))
    ypp_diff_p = t.sf(np.absolute(ypp_diff_t), n - 1)
    return ypp_diff_t, ypp_diff_p

def paired_wilcoxon_on_errors(newprobs, oldprobs, ytrue):
    #computes paired wilcoxon on errors (not clear if valid for classification)
    newprobs_res_abs = np.absolute(array(ytrue) - array(newprobs))
    oldprobs_res_abs = np.absolute(array(ytrue) - array(oldprobs))
    print(newprobs_res_abs)
    stat, p = wilcoxon(newprobs_res_abs, oldprobs_res_abs, alternative="greater")
    print(stat, p)
    return p

def paired_permutation_1tail_on_aucs(newprobs, oldprobs, ytrue, multiclass=False, classes = None, iters = 3000):
    #computes p-value based on permutation test (an exact test)
    #this is not correct; do not use. 
    n = len(ytrue)
    target_auc = computeAUC(ytrue, newprobs, multiclass,  classes = classes)

    criteria_met = 0 #counts how frequent auc surpassed
    if len(newprobs.shape) < 2:
        newprobs = newprobs.reshape((n, 1))
    if len(oldprobs.shape) < 2:
        oldprobs = oldprobs.reshape((n, 1))
    for i in range(iters):
        mask = np.random.randint(2, size=n).reshape((n, 1))#does random permutation of what is in new versus old
        this_newprobs = newprobs*mask + oldprobs*(1-mask)
        this_auc = computeAUC(ytrue, this_newprobs, multiclass,  classes = classes)
        if this_auc > target_auc:
            criteria_met += 1
    p = criteria_met / float(iters)
    #print("\n-----\n", p, bootstrap_1tail_on_aucs_bothprobs(newprobs[:,-1], oldprobs[:,-1], ytrue, multiclass, classes, iters))
    return p

def permutation_1tail_on_aucs(ytrue, ypredProbs, multiclass=False, classes=None, iters=8000):
    #computes p-value based on permuation
    n = len(ytrue) 
    ytrue = np.array(ytrue)
    target_auc = computeAUC(ytrue, ypredProbs, multiclass,  classes = classes)
    criteria_met = 0 #counts how frequent old auc surpassed new auc
    allids = np.random.randint(n, size=(iters, n))
    for i in range(iters):
        this_probs = np.random.permutation(ypredProbs)
        this_newauc = computeAUC(ytrue, this_probs, multiclass,  classes = classes)
        if this_newauc > target_auc:
            criteria_met += 1
    return criteria_met / float(iters)

    

def paired_bootstrap_1tail_on_aucs(newprobs, oldprobs, ytrue, multiclass=False, classes = None, iters = 8000):
    #computes p-value based on paired bootstrap 
    n = len(ytrue)
    ytrue = np.array(ytrue)
    criteria_met = 0 #counts how frequent old auc surpassed new auc
    allids = np.random.randint(n, size=(iters, n))
    for i in range(iters):
        ids = allids[i]
        this_ytrue = ytrue[ids]
        this_newprobs = newprobs[ids]
        this_oldprobs = oldprobs[ids]
        # this_newauc = computeAUC(this_ytrue, this_newprobs.reshape([n,1]), multiclass,  classes = classes)
        # this_oldauc = computeAUC(this_ytrue, this_oldprobs.reshape([n,1]), multiclass,  classes = classes)
        this_newauc = computeAUC(this_ytrue, this_newprobs, multiclass,  classes = classes)
        this_oldauc = computeAUC(this_ytrue, this_oldprobs, multiclass,  classes = classes)
        if this_newauc < this_oldauc:
            criteria_met += 1
    return criteria_met / float(iters)
