
# Built-in
import os
import warnings
import itertools as itt
import copy
import datetime as dtm      # DB

# Common
import numpy as np
import scipy.optimize as scpopt
import scipy.interpolate as scpinterp
import scipy.constants as scpct
import scipy.sparse as sparse
from scipy.interpolate import BSpline
import scipy.stats as scpstats
import matplotlib.pyplot as plt


# ToFu-specific
import tofu.utils as utils
from . import _fit12d_funccostjac as _funccostjac
from . import _plot


__all__ = ['fit1d_dinput', 'fit2d_dinput',
           'fit12d_dvalid', 'fit12d_dscales',
           'fit1d', 'fit2d',
           'fit1d_extract', 'fit2d_extract']


_NPEAKMAX = 12
_DCONSTRAINTS = {'amp': False,
                 'width': False,
                 'shift': False,
                 'double': False,
                 'symmetry': False}
_SAME_SPECTRUM = False
_DEG = 2
_NBSPLINES = 13
_TOL1D = {'x': 1e-10, 'f': 1.e-10, 'g': 1.e-10}
_TOL2D = {'x': 1e-6, 'f': 1.e-6, 'g': 1.e-6}
_SYMMETRY_CENTRAL_FRACTION = 0.3
_BINNING = False
_POS = False
_SUBSET = False
_CHAIN = True
_METHOD = 'trf'
_LOSS = 'linear'
_D3 = {'amp': 'x', 'coefs': 'lines', 'ratio': 'lines',
       'Ti': 'x', 'width': 'lines',
       'vi': 'x', 'shift': 'lines'}
_VALID_NSIGMA = 6.
_VALID_FRACTION = 0.8
_SIGMA_MARGIN = 3.
_ALLOW_PICKLE = True
_LTYPES = [int, float, np.int_, np.float_]


###########################################################
###########################################################
#
#           Preliminary
#       utility tools for 1d spectral fitting
#
###########################################################
###########################################################

# DEPRECATED !!!!!!!!!!!!!!!!!
def get_peaks(x, y, nmax=None):
    """ Automatically find peaks in spectrum """

    raise Exception("Deprecated!")

    if nmax is None:
        nmax = _NPEAKMAX

    # Prepare
    ybis = np.copy(y)
    A = np.empty((nmax,), dtype=y.dtype)
    x0 = np.empty((nmax,), dtype=x.dtype)
    sigma = np.empty((nmax,), dtype=y.dtype)
    def gauss(xx, A, x0, sigma): return A*np.exp(-(xx-x0)**2/sigma**2)
    def gauss_jac(xx, A, x0, sigma):
        jac = np.empty((xx.size, 3), dtype=float)
        jac[:, 0] = np.exp(-(xx-x0)**2/sigma**2)
        jac[:, 1] = A*2*(xx-x0)/sigma**2 * np.exp(-(xx-x0)**2/sigma**2)
        jac[:, 2] = A*2*(xx-x0)**2/sigma**3 * np.exp(-(xx-x0)**2/sigma**2)
        return jac

    dx = np.nanmin(np.diff(x))

    # Loop
    nn = 0
    while nn < nmax:
        ind = np.nanargmax(ybis)
        x00 = x[ind]
        if np.any(np.diff(ybis[ind:], n=2) >= 0.):
            wp = min(x.size-1,
                     ind + np.nonzero(np.diff(ybis[ind:],n=2)>=0.)[0][0] + 1)
        else:
            wp = ybis.size-1
        if np.any(np.diff(ybis[:ind+1], n=2) >= 0.):
            wn = max(0, np.nonzero(np.diff(ybis[:ind+1],n=2)>=0.)[0][-1] - 1)
        else:
            wn = 0
        width = x[wp]-x[wn]
        assert width>0.
        indl = np.arange(wn, wp+1)
        sig = np.ones((indl.size,))
        if (np.abs(np.mean(np.diff(ybis[ind:wp+1])))
            > np.abs(np.mean(np.diff(ybis[wn:ind+1])))):
            sig[indl < ind] = 1.5
            sig[indl > ind] = 0.5
        else:
            sig[indl < ind] = 0.5
            sig[indl > ind] = 1.5
        p0 = (ybis[ind], x00, width)#,0.)
        bounds = (np.r_[0., x[wn], dx/2.],
                  np.r_[5.*ybis[ind], x[wp], 5.*width])
        try:
            (Ai, x0i, sigi) = scpopt.curve_fit(gauss, x[indl], ybis[indl],
                                               p0=p0, bounds=bounds, jac=gauss_jac,
                                               sigma=sig, x_scale='jac')[0]
        except Exception as err:
            print(str(err))
            import ipdb
            ipdb.set_trace()
            pass

        ybis = ybis - gauss(x, Ai, x0i, sigi)
        A[nn] = Ai
        x0[nn] = x0i
        sigma[nn] = sigi


        nn += 1
    return A, x0, sigma


def get_symmetry_axis_1dprofile(phi, data, cent_fraction=None):
    """ On a series of 1d vertical profiles, find the best symmetry axis """

    if cent_fraction is None:
        cent_fraction  = _SYMMETRY_CENTRAL_FRACTION

    # Find the phi in the central fraction
    phimin = np.nanmin(phi)
    phimax = np.nanmax(phi)
    phic = 0.5*(phimax + phimin)
    dphi = (phimax - phimin)*cent_fraction
    indphi = np.abs(phi-phic) <= dphi/2.
    phiok = phi[indphi]

    # Compute new phi and associated costs
    phi2 = phi[:, None] - phiok[None, :]
    phi2min = np.min([np.nanmax(np.abs(phi2 * (phi2<0)), axis=0),
                      np.nanmax(np.abs(phi2 * (phi2>0)), axis=0)], axis=0)
    indout = np.abs(phi2) > phi2min[None, :]
    phi2p = np.abs(phi2)
    phi2n = np.abs(phi2)
    phi2p[(phi2<0) | indout] = np.nan
    phi2n[(phi2>0) | indout] = np.nan
    nok = np.min([np.sum((~np.isnan(phi2p)), axis=0),
                  np.sum((~np.isnan(phi2n)), axis=0)], axis=0)
    cost = np.full((data.shape[0], phiok.size), np.nan)
    for ii in range(phiok.size):
        indp = np.argsort(np.abs(phi2p[:, ii]))
        indn = np.argsort(np.abs(phi2n[:, ii]))
        cost[:, ii] = np.nansum(
            (data[:, indp] - data[:, indn])[:, :nok[ii]]**2,
            axis=1)
    return phiok[np.nanargmin(cost, axis=1)]


###########################################################
###########################################################
#
#           1d spectral fitting from dlines
#
###########################################################
###########################################################


def _checkformat_dconstraints(dconstraints=None, defconst=None):
    # Check constraints
    if dconstraints is None:
        dconstraints =  defconst

    # Check dconstraints keys
    lk = sorted(_DCONSTRAINTS.keys())
    c0= (isinstance(dconstraints, dict)
         and all([k0 in lk for k0 in dconstraints.keys()]))
    if not c0:
        msg = (
            "\ndconstraints should contain constraints for spectrum fitting\n"
            + "It be a dict with the following keys:\n"
            + "\t- available keys: {}\n".format(lk)
            + "\t- provided keys: {}".format(dconstraints.keys())
        )
        raise Exception(msg)

    # copy to avoid modifying reference
    return copy.deepcopy(dconstraints)


def _dconstraints_double(dinput, dconstraints, defconst=_DCONSTRAINTS):
    dinput['double'] = dconstraints.get('double', defconst['double'])
    c0 = (
        isinstance(dinput['double'], bool)
        or (
            isinstance(dinput['double'], dict)
            and all([
                kk in ['dratio', 'dshift'] and type(vv) in _LTYPES
                for kk, vv in dinput['double'].items()
            ])
        )
    )
    if c0 is False:
        msg = ("dconstraints['double'] must be either:\n"
               + "\t- False: no line doubling\n"
               + "\t- True:  line doublin with unknown ratio and shift\n"
               + "\t- {'dratio': float}: line doubling with:\n"
               + "\t  \t explicit ratio, unknown shift\n"
               + "\t- {'dshift': float}: line doubling with:\n"
               + "\t  \t unknown ratio, explicit shift\n"
               + "\t- {'dratio': floati, 'dshift': float}: line doubling with:\n"
               + "\t  \t explicit ratio, explicit shift")
        raise Exception(msg)


def _width_shift_amp(indict, keys=None, dlines=None, nlines=None, k0=None):

    # ------------------------
    # Prepare error message
    msg = ''
    pavail = sorted(set(itt.chain.from_iterable([
        v0.keys() for v0 in dlines.values()
    ])))

    # ------------------------
    # Check case
    c0 = indict is False
    c1 = (
        isinstance(indict, str)
        and indict in pavail
    )
    c2 = (
        isinstance(indict, dict)
        and all([
            isinstance(k0, str)
            and (
                (isinstance(v0, str) and v0 in keys)
                or (
                    isinstance(v0, list)
                    and all([
                        isinstance(v1, str) and v1 in keys for v1 in v0
                    ])
                )
            )
            for k0, v0 in indict.items()
        ])
    )
    c3 = (
        isinstance(indict, dict)
        and all([
            ss in keys
            and isinstance(vv, dict)
            and all([s1 in ['key', 'coef', 'offset'] for s1 in vv.keys()])
            and isinstance(vv['key'], str)
            for ss, vv in indict.items()
        ])
    )
    c4 = (
        isinstance(indict, dict)
        and isinstance(indict.get('keys'), list)
        and isinstance(indict.get('ind'), np.ndarray)
    )
    if not any([c0, c1, c2, c3, c4]):
        msg = (
            "dconstraints['{}'] shoud be either:\n".format(k0)
            + "\t- False ({}): no constraint\n".format(c0)
            + "\t- str ({}): key from dlines['<lines>'] ".format(c1)
            + "to be used as criterion\n"
            + "\t\t available crit: {}\n".format(pavail)
            + "\t- dict ({}): ".format(c2)
            + "{str: line_keyi or [line_keyi, ..., line_keyj}\n"
            + "\t- dict ({}): ".format(c3)
            + "{line_keyi: {'key': str, 'coef': , 'offset': }}\n"
            + "\t- dict ({}): ".format(c4)
            + "{'keys': [], 'ind': np.ndarray}\n"
            + "  Available line_keys:\n{}\n".format(sorted(keys))
            + "  You provided:\n{}".format(indict)
        )
        raise Exception(msg)

    # ------------------------
    # str key to be taken from dlines as criterion
    if c0:
        lk = keys
        ind = np.eye(nlines)
        outdict = {'keys': np.r_[lk], 'ind': ind,
                   'coefs': np.ones((nlines,)),
                   'offset': np.zeros((nlines,))}

    if c1:
        lk = sorted(set([dlines[k0].get(indict, k0)
                         for k0 in keys]))
        ind = np.array([[dlines[k1].get(indict, k1) == k0
                         for k1 in keys] for k0 in lk])
        outdict = {'keys': np.r_[lk], 'ind': ind,
                   'coefs': np.ones((nlines,)),
                   'offset': np.zeros((nlines,))}

    elif c2:
        lkl = []
        for k0, v0 in indict.items():
            if isinstance(v0, str):
                v0 = [v0]
            if not (len(set(v0)) == len(v0)
                    and all([k1 not in lkl for k1 in v0])):
                msg = ("Inconsistency in indict[{}], either:\n".format(k0)
                       + "\t- v0 not unique: {}\n".format(v0)
                       + "\t- some v0 not in keys: {}\n".format(keys)
                       + "\t- some v0 in lkl:      {}".format(lkl))
                raise Exception(msg)
            indict[k0] = v0
            lkl += v0
        for k0 in set(keys).difference(lkl):
            indict[k0] = [k0]
        lk = sorted(set(indict.keys()))
        ind = np.array([[k1 in indict[k0] for k1 in keys] for k0 in lk])
        outdict = {'keys': np.r_[lk], 'ind': ind,
                   'coefs': np.ones((nlines,)),
                   'offset': np.zeros((nlines,))}

    elif c3:
        lk = sorted(set([v0['key'] for v0 in indict.values()]))
        lk += sorted(set(keys).difference(indict.keys()))
        ind = np.array([[indict.get(k1, {'key': k1})['key'] == k0
                         for k1 in keys]
                        for k0 in lk])
        coefs = np.array([indict.get(k1, {'coef': 1.}).get('coef', 1.)
                          for k1 in keys])
        offset = np.array([indict.get(k1, {'offset': 0.}).get('offset', 0.)
                           for k1 in keys])
        outdict = {'keys': np.r_[lk], 'ind': ind,
                   'coefs': coefs,
                   'offset': offset}

    elif c4:
        outdict = indict
        if 'coefs' not in indict.keys():
            outdict['coefs'] = np.ones((nlines,))
        if 'offset' not in indict.keys():
            outdict['offset'] = np.zeros((nlines,))

    # ------------------------
    # Ultimate conformity checks
    if not c0:
        assert sorted(outdict.keys()) == ['coefs', 'ind', 'keys', 'offset']
        assert isinstance(outdict['ind'], np.ndarray)
        assert outdict['ind'].dtype == np.bool_
        assert outdict['ind'].shape == (outdict['keys'].size, nlines)
        assert np.all(np.sum(outdict['ind'], axis=0) == 1)
        assert outdict['coefs'].shape == (nlines,)
        assert outdict['offset'].shape == (nlines,)

    return outdict


###########################################################
###########################################################
#
#           2d spectral fitting from dlines
#
###########################################################
###########################################################


def _dconstraints_symmetry(dinput, symmetry=None, dataphi1d=None, phi1d=None,
                           cent_fraction=None, defconst=_DCONSTRAINTS):
    if symmetry is None:
        symmetry = defconst['symmetry']
    dinput['symmetry'] = symmetry
    if not isinstance(dinput['symmetry'], bool):
        msg = "dconstraints['symmetry'] must be a bool"
        raise Exception(msg)

    if dinput['symmetry'] is True:
        dinput['symmetry_axis'] = get_symmetry_axis_1dprofile(
            phi1d, dataphi1d, cent_fraction=cent_fraction)


###########################################################
###########################################################
#
#           data, lamb, phi conformity checks
#
###########################################################
###########################################################


def _checkformat_data_fit12d_dlines_msg(data, lamb, phi=None, mask=None):
    datash = data.shape if isinstance(data, np.ndarray) else type(data)
    lambsh = lamb.shape if isinstance(lamb, np.ndarray) else type(lamb)
    phish = phi.shape if isinstance(phi, np.ndarray) else type(phi)
    masksh = mask.shape if isinstance(mask, np.ndarray) else type(mask)
    shaped = '(nt, n1)' if phi is None else '(nt, n1, n2)'
    shape = '(n1,)' if phi is None else '(n1, n2)'
    msg = ("Args data, lamb, phi and mask must be:\n"
           + "\t- data: {} or {} np.ndarray\n".format(shaped, shape)
           + "\t- lamb, phi: both {} np.ndarray\n".format(shape)
           + "\t- mask: None or {}\n".format(shape)
           + "  You provided:\n"
           + "\t - data: {}\n".format(datash)
           + "\t - lamb: {}\n".format(lambsh))
    if phi is not None:
        msg += "\t - phi: {}\n".format(phish)
    msg += "\t - mask: {}\n".format(masksh)
    return msg


def _checkformat_data_fit12d_dlines(data, lamb, phi=None,
                                   nxi=None, nxj=None, mask=None):

    # Check types
    c0 = (isinstance(data, np.ndarray)
          and isinstance(lamb, np.ndarray))
    if phi is not None:
        c0 &= isinstance(phi, np.ndarray)

    if not c0:
        msg = _checkformat_data_fit12d_dlines_msg(data, lamb,
                                                  phi=phi, mask=mask)
        raise Exception(msg)

    # Check shapes 1
    mindim = 1 if phi is None else 2
    c0 = (data.ndim in mindim + np.r_[0, 1]
          and lamb.ndim == mindim
          and lamb.shape == data.shape[-mindim:])
    if phi is not None:
        c0 &= (lamb.ndim == phi.ndim
               and lamb.shape == phi.shape
               and lamb.shape in [(nxi, nxj), (nxj, nxi)])

    if not c0:
        msg = _checkformat_data_fit12d_dlines_msg(data, lamb,
                                                  phi=phi, mask=mask)
        raise Exception(msg)

    # Check shapes 2
    if data.ndim == mindim:
        data = data[None, ...]
    if phi is not None and lamb.shape == (nxj, nxi):
        lamb = lamb.T
        phi = phi.T
        data = np.swapaxes(data, 1, 2)

    # mask
    if mask is not None:
        if mask.shape != lamb.shape:
            if phi is not None and mask.T.shape == lamb.shape:
                mask = mask.T
            else:
                msg = _checkformat_data_fit12d_dlines_msg(data, lamb,
                                                          phi=phi, mask=mask)
                raise Exception(msg)
    return lamb, phi, data, mask


###########################################################
###########################################################
#
#           Domain limitation
#
###########################################################
###########################################################


def _checkformat_domain(domain=None, keys=['lamb', 'phi']):

    if keys is None:
        keys = ['lamb', 'phi']
    if isinstance(keys, str):
        keys = [keys]

    if domain is None:
        domain = {k0: {'spec': [np.inf*np.r_[-1., 1.]]} for k0 in keys}
        return domain

    c0 = (isinstance(domain, dict)
          and all([k0 in keys for k0 in domain.keys()]))
    if not c0:
        msg = ("Arg domain must be a dict with keys {}\n".format(keys)
               + "\t- provided: {}".format(domain))
        raise Exception(msg)

    domain2 = {k0: v0 for k0, v0 in domain.items()}
    for k0 in keys:
        domain2[k0] = domain2.get(k0, [np.inf*np.r_[-1., 1.]])

    ltypesin = [list, np.ndarray]
    ltypesout = [tuple]
    for k0, v0 in domain2.items():
        c0 = (type(v0) in ltypesin + ltypesout
              and (all([(type(v1) in ltypesin + ltypesout
                         and len(v1) == 2
                         and v1[1] > v1[0]) for v1 in v0])
                   or (len(v0) == 2 and v0[1] > v0[0])))
        if not c0:
            msg = ("domain[{}] must be either a:\n".format(k0)
                   + "\t- np.ndarray or list of 2 increasing values: "
                    + "inclusive interval\n"
                   + "\t- tuple of 2 increasing values: exclusive interval\n"
                   + "\t- a list of combinations of the above\n"
                   + "  provided: {}".format(v0))
            raise Exception(msg)

        if type(v0) in ltypesout:
            v0 = [v0]
        else:
            c0 = all([(type(v1) in ltypesin + ltypesout
                       and len(v1) == 2
                       and v1[1] > v1[0]) for v1 in v0])
            if not c0:
                v0 = [v0]
        domain2[k0] = {'spec': v0,
                       'minmax': [np.nanmin(v0), np.nanmax(v0)]}
    return domain2


def apply_domain(lamb=None, phi=None, domain=None):

    lc = [lamb is not None, phi is not None]
    if not lc[0]:
        msg = "At least lamb must be provided!"
        raise Exception(msg)

    din = {'lamb': lamb}
    if lc[1]:
        din['phi'] = phi

    domain = _checkformat_domain(domain=domain, keys=din.keys())
    ind = np.ones(lamb.shape, dtype=bool)
    for k0, v0 in din.items():
        indin = np.zeros(v0.shape, dtype=bool)
        indout = np.zeros(v0.shape, dtype=bool)
        for v1 in domain[k0]['spec']:
            indi = (v0 >= v1[0]) & (v0 <= v1[1])
            if isinstance(v1, tuple):
                indout |= indi
            else:
                indin |= indi
        ind = ind & indin & (~indout)
    return ind, domain


###########################################################
###########################################################
#
#           binning (2d only)
#
###########################################################
###########################################################


def _binning_check(binning, nlamb=None, nphi=None,
                   domain=None, nbsplines=None, deg=None):
    lk = ['phi', 'lamb']
    lkall = lk + ['nperbin']
    msg = ("binning must be dict of the form:\n"
           + "\t- provide number of bins:\n"
           + "\t  \t{'phi':  int,\n"
           + "\t  \t 'lamb': int}\n"
           + "\t- provide bin edges vectors:\n"
           + "\t  \t{'phi':  1d np.ndarray (increasing),\n"
           + "\t  \t 'lamb': 1d np.ndarray (increasing)}\n"
           + "  provided:\n{}".format(binning))

    # Check input
    if binning is None:
        binning = _BINNING
    if nbsplines is None:
        nbsplines = False
    if nbsplines is not False:
        c0 = isinstance(nbsplines, int) and nbsplines > 0
        if not c0:
            msg2 = ("Both nbsplines and deg must be positive int!\n"
                    + "\t- nbsplines: {}\n".format(nbsplines))
            raise Exception(msg2)

    # Check which format was passed and return None or dict
    ltypes0 = _LTYPES
    ltypes1 = [tuple, list, np.ndarray]
    lc = [binning is False,
          (isinstance(binning, dict)
           and all([kk in lkall for kk in binning.keys()])),
          type(binning) in ltypes0,
          type(binning) in ltypes1]
    if not any(lc):
        raise Exception(msg)
    if binning is False:
        return binning
    elif type(binning) in ltypes0:
        binning = {'phi': {'nbins': int(binning)},
                   'lamb': {'nbins': int(binning)}}
    elif type(binning) in ltypes1:
        binning = np.atleast_1d(binning).ravel()
        binning = {'phi': {'edges': binning},
                   'lamb': {'edges': binning}}
    for kk in lk:
        if type(binning[kk]) in ltypes0:
            binning[kk] = {'nbins': int(binning[kk])}
        elif type(binning[kk]) in ltypes1:
            binning[kk] = {'edges': np.atleast_1d(binning[kk]).ravel()}

    c0 = all([all([k1 in ['edges', 'nbins'] for k1 in binning[k0].keys()])
              for k0 in lk])
    c0 = (c0 and
          all([((binning[k0].get('nbins') is None
                 or type(binning[k0].get('nbins')) in ltypes0)
                and (binning[k0].get('edges') is None
                 or type(binning[k0].get('edges')) in ltypes1))
              for k0 in lk]))
    if not c0:
        raise Exception(msg)

    # Check dict
    for k0 in lk:
        c0 = all([k1 in ['nbins', 'edges'] for k1 in binning[k0].keys()])
        if not c0:
            raise Exception(msg)
        if binning[k0].get('nbins') is not None:
            binning[k0]['nbins'] = int(binning[k0]['nbins'])
            if binning[k0].get('edges') is None:
                binning[k0]['edges'] = np.linspace(
                    domain[k0]['minmax'][0], domain[k0]['minmax'][1],
                    binning[k0]['nbins'] + 1, endpoint=True)
            else:
                binning[k0]['edges'] = np.atleast_1d(
                    binning[k0]['edges']).ravel()
                if binning[k0]['nbins'] != binning[k0]['edges'].size - 1:
                    raise Exception(msg)
        elif binning[k0].get('bin_edges') is not None:
            binning[k0]['edges'] = np.atleast_1d(binning[k0]['edges']).ravel()
            binning[k0]['nbins'] = binning[k0]['edges'].size - 1
        else:
            raise Exception(msg)

        if not np.allclose(binning[k0]['edges'],
                           np.unique(binning[k0]['edges'])):
            raise Exception(msg)

    # Optional check vs nbsplines and deg
    if nbsplines is not False:
        if binning['phi']['nbins'] <= nbsplines:
            msg = ("The number of bins is too high:\n"
                   + "\t- nbins =     {}\n".format(binning['phi']['nbins'])
                   + "\t- nbsplines = {}".format(nbsplines))
            raise Exception(msg)
    return binning


def binning_2d_data(lamb, phi, data, indok=None,
                    domain=None, binning=None, nbsplines=None):

    # ------------------
    # Checkformat input
    binning = _binning_check(binning, domain=domain, nbsplines=nbsplines)
    if binning is False:
        return lamb, phi, data, indok, binning

    nphi = binning['phi']['nbins']
    nlamb = binning['lamb']['nbins']
    bins = (binning['lamb']['edges'], binning['phi']['edges'])
    nspect = data.shape[0]
    npts = nlamb*nphi

    # ------------------
    # Compute

    databin = scpstats.binned_statistic_2d(
        lamb[indok], phi[indok], data[:, indok],
        statistic='sum', bins=bins,
        range=None, expand_binnumbers=True)[0]
    nperbin = scpstats.binned_statistic_2d(
        lamb[indok], phi[indok], np.ones((indok.sum(),), dtype=int),
        statistic='sum', bins=bins,
        range=None, expand_binnumbers=True)[0]
    binning['nperbin'] = nperbin

    lambbin = 0.5*(binning['lamb']['edges'][1:]
                   + binning['lamb']['edges'][:-1])
    phibin = 0.5*(binning['phi']['edges'][1:]
                  + binning['phi']['edges'][:-1])
    lambbin = np.repeat(lambbin[:, None], nphi, axis=1)
    phibin = np.repeat(phibin[None, :], nlamb, axis=0)
    indok = np.any(~np.isnan(databin), axis=0)

    return lambbin, phibin, databin, indok, binning


###########################################################
###########################################################
#
#           dprepare dict
#
###########################################################
###########################################################


def _get_subset_indices(subset, indlogical):
    if subset is None:
        subset = _SUBSET
    if subset is False:
        return indlogical

    c0 = ((isinstance(subset, np.ndarray)
           and subset.shape == indlogical.shape
           and 'bool' in subset.dtype.name)
          or (type(subset) in [int, float, np.int_, np.float_]
              and subset >= 0))
    if not c0:
        msg = ("subset must be either:\n"
               + "\t- an array of bool of shape: {}\n".format(indlogical.shape)
               + "\t- a positive int (nb. of ind. to keep from indlogical)\n"
               + "You provided:\n{}".format(subset))
        raise Exception(msg)

    if isinstance(subset, np.ndarray):
        indlogical = subset & indlogical
    else:
        subset = np.random.default_rng().choice(
            indlogical.sum(), size=int(indlogical.sum() - subset),
            replace=False, shuffle=False)
        ind = indlogical.nonzero()
        indlogical[ind[0][subset], ind[1][subset]] = False
    return indlogical


def _extract_lphi_spectra(data, phi, lamb,
                          lphi=None, lphi_tol=None,
                          databin=None, binning=None, nlamb=None):
    """ Extra several 1d spectra from 2d image at lphi """

    # --------------
    # Check input
    if lphi is None:
        lphi = False
    if lphi is False:
        lphi_tol = False
    if lphi is not False:
        lphi = np.atleast_1d(lphi).astype(float).ravel()
        lphi_tol = float(lphi_tol)

    if lphi is False:
        return False, False
    nphi = len(lphi)

    # --------------
    # Compute non-trivial cases

    if binning is False:
        if nlamb is None:
            nlamb = lamb.shape[0]
        lphi_lamb = np.linspace(lamb.min(), lamb.max(), nlamb+1)
        lphi_spectra = np.full((data.shape[0], lphi_lamb.size-1, nphi), np.nan)
        for ii in range(nphi):
            indphi = np.abs(phi - lphi[ii]) < lphi_tol
            lphi_spectra[:, :, ii] = scpstats.binned_statistic(
                lamb[indphi], data[:, indphi], bins=lphi_lamb,
                statistic='mean', range=None)[0]

    else:
        lphi_lamb = 0.5*(binning['lamb']['edges'][1:]
                         + binning['lamb']['edges'][:-1])
        lphi_phi = 0.5*(binning['phi']['edges'][1:]
                        + binning['phi']['edges'][:-1])
        lphi_spectra = np.full((data.shape[0], lphi_lamb.size, nphi), np.nan)
        lphi_spectra1 = np.full((data.shape[0], lphi_lamb.size, nphi), np.nan)
        for ii in range(nphi):
            datai = databin[:, :, np.abs(lphi_phi - lphi[ii]) < lphi_tol]
            iok = np.any(~np.isnan(datai), axis=2)
            for jj in range(datai.shape[0]):
                if np.any(iok[jj, :]):
                    lphi_spectra[jj, iok[jj, :], ii] = np.nanmean(
                        datai[jj, iok[jj, :], :], axis=1)

    return lphi_spectra, lphi_lamb


def _checkformat_possubset(pos=None, subset=None):
    if pos is None:
        pos = _POS
    c0 = isinstance(pos, bool) or type(pos) in _LTYPES
    if not c0:
        msg = ("Arg pos must be either:\n"
               + "\t- False: no positivity constraints\n"
               + "\t- True: all negative values are set to nan\n"
               + "\t- float: all negative values are set to pos")
        raise Exception(msg)
    if subset is None:
        subset = _SUBSET
    return pos, subset


def multigausfit1d_from_dlines_prepare(data=None, lamb=None,
                                       mask=None, domain=None,
                                       pos=None, subset=None):

    # --------------
    # Check input
    pos, subset = _checkformat_possubset(pos=pos, subset=subset)

    # Check shape of data (multiple time slices possible)
    lamb, _, data, mask = _checkformat_data_fit12d_dlines(data, lamb,
                                                          mask=mask)

    # --------------
    # Use valid data only and optionally restrict lamb
    indok, domain = apply_domain(lamb, domain=domain)
    if mask is not None:
        indok &= mask

    # Optional positivity constraint
    if pos is not False:
        if pos is True:
            data[data < 0.] = np.nan
        else:
            data[data < 0.] = pos

    # Introduce time-dependence (useful for valid)
    indok &= np.any(~np.isnan(data), axis=0)

    # Recompute domain
    domain['lamb']['minmax'] = [np.nanmin(lamb[indok]), np.nanmax(lamb[indok])]

    # --------------
    # Optionally fit only on subset
    # randomly pick subset indices (replace=False => no duplicates)
    indok = _get_subset_indices(subset, indok)

    # --------------
    # Return
    dprepare = {'data': data, 'lamb': lamb,
                'domain': domain, 'indok': indok,
                'pos': pos, 'subset': subset}
    return dprepare


def multigausfit2d_from_dlines_prepare(data=None, lamb=None, phi=None,
                                       mask=None, domain=None,
                                       pos=None, binning=None,
                                       nbsplines=None, subset=None,
                                       nxi=None, nxj=None,
                                       lphi=None, lphi_tol=None):

    # --------------
    # Check input
    pos, subset = _checkformat_possubset(pos=pos, subset=subset)

    # Check shape of data (multiple time slices possible)
    lamb, phi, data, mask = _checkformat_data_fit12d_dlines(
        data, lamb, phi,
        nxi=nxi, nxj=nxj, mask=mask)

    # --------------
    # Use valid data only and optionally restrict lamb / phi
    indok, domain = apply_domain(lamb, phi, domain=domain)
    if mask is not None:
        indok &= mask

    # Optional positivity constraint
    if pos is not False:
        if pos is True:
            data[data < 0.] = np.nan
        else:
            data[data < 0.] = pos

    # Introduce time-dependence (useful for valid)
    indok &= np.any(~np.isnan(data), axis=0)

    # Recompute domain
    domain['lamb']['minmax'] = [np.nanmin(lamb[indok]), np.nanmax(lamb[indok])]
    domain['phi']['minmax'] = [np.nanmin(phi[indok]), np.nanmax(phi[indok])]

    # --------------
    # Optionnal 2d binning
    lambbin, phibin, databin, indok, binning = binning_2d_data(
        lamb, phi, data, indok=indok,
        binning=binning, domain=domain, nbsplines=nbsplines)

    # --------------
    # Optionally fit only on subset
    # randomly pick subset indices (replace=False => no duplicates)
    indok = _get_subset_indices(subset, indok)

    # --------------
    # Optionally extract 1d spectra at lphi
    lphi_spectra, lphi_lamb = _extract_lphi_spectra(data, phi, lamb,
                                                    lphi, lphi_tol,
                                                    databin=databin,
                                                    binning=binning)

    # --------------
    # Return
    dprepare = {'data': databin, 'lamb': lambbin, 'phi': phibin,
                'domain': domain, 'binning': binning, 'indok': indok,
                'pos': pos, 'subset': subset, 'nxi': nxi, 'nxj': nxj,
                'lphi': lphi, 'lphi_tol': lphi_tol,
                'lphi_spectra': lphi_spectra, 'lphi_lamb': lphi_lamb}
    return dprepare


def multigausfit2d_from_dlines_dbsplines(knots=None, deg=None, nbsplines=None,
                                         phimin=None, phimax=None,
                                         symmetryaxis=None):
    # Check / format input
    if nbsplines is None:
        nbsplines = _NBSPLINES
    c0 = [nbsplines is False, isinstance(nbsplines, int)]
    if not any(c0):
        msg = "nbsplines must be a int (the degree of the bsplines to be used!)"
        raise Exception(msg)

    if nbsplines is False:
        lk = ['knots', 'knots_mult', 'nknotsperbs', 'ptsx0', 'nbs', 'deg']
        return dict.fromkeys(lk, False)

    if deg is None:
        deg = _DEG
    if not (isinstance(deg, int) and deg <= 3):
        msg = "deg must be a int <= 3 (the degree of the bsplines to be used!)"
        raise Exception(msg)
    if symmetryaxis is None:
        symmetryaxis = False

    if knots is None:
        if phimin is None or phimax is None:
            msg = "Please provide phimin and phimax if knots is not provided!"
            raise Exception(msg)
        if symmetryaxis is False:
            knots = np.linspace(phimin, phimax, nbsplines + 1 - deg)
        else:
            symax = np.nanmean(symmetryaxis)
            phi2max = np.max(np.abs(np.r_[phimin, phimax] - symax))
            knots = np.linspace(0, phi2max, nbsplines + 1 - deg)

    if not np.allclose(knots, np.unique(knots)):
        msg = "knots must be a vector of unique values!"
        raise Exception(msg)

    # Get knots for scipy (i.e.: with multiplicity)
    if deg > 0:
        knots_mult = np.r_[[knots[0]]*deg, knots, [knots[-1]]*deg]
    else:
        knots_mult = knots
    nknotsperbs = 2 + deg
    nbs = knots.size - 1 + deg
    assert nbs == knots_mult.size - 1 - deg

    if deg == 0:
        ptsx0 = 0.5*(knots[:-1] + knots[1:])
    elif deg == 1:
        ptsx0 = knots
    elif deg == 2:
        num = (knots_mult[3:]*knots_mult[2:-1]
               - knots_mult[1:-2]*knots_mult[:-3])
        denom = (knots_mult[3:] + knots_mult[2:-1]
                 - knots_mult[1:-2] - knots_mult[:-3])
        ptsx0 = num / denom
    else:
        # To be derived analytically for more accuracy
        ptsx0 = np.r_[knots[0],
                      np.mean(knots[:2]),
                      knots[1:-1],
                      np.mean(knots[-2:]),
                      knots[-1]]
        msg = ("degree 3 not fully implemented yet!"
               + "Approximate values for maxima positions")
        warnings.warn(msg)
    assert ptsx0.size == nbs
    dbsplines = {'knots': knots, 'knots_mult': knots_mult,
                 'nknotsperbs': nknotsperbs, 'ptsx0': ptsx0,
                 'nbs': nbs, 'deg': deg}
    return dbsplines


###########################################################
###########################################################
#
#           dvalid dict (S/N ratio)
#
###########################################################
###########################################################


def _dvalid_checkfocus_errmsg(focus=None, focus_half_width=None,
                              lines_keys=None):
    msg = ("Please provide focus as:\n"
           + "\t- str: the key of an available spectral line:\n"
           + "\t\t{}\n".format(lines_keys)
           + "\t- float: a wavelength value\n"
           + "\t- a list / tuple / flat np.ndarray of such\n"
           + "  You provided:\n"
           + "{}\n\n".format(focus)
           + "Please provide focus_half_width as:\n"
           + "\t- float: a unique wavelength value for all focus\n"
           + "\t- a list / tuple / flat np.ndarray of such\n"
           + "  You provided:\n"
           + "{}".format(focus_half_width))
    return msg


def _dvalid_checkfocus(focus=None, focus_half_width=None,
                       lines_keys=None, lines_lamb=None):
    """ Check the provided focus is properly formatted and convert it

    focus specifies the wavelength range of interest in which S/N is evaluated
    It can be provided as:
        - a spectral line key (or list of such)
        - a wavelength (or list of such)

    For each wavelength, a spectral range centered on it, is defined using
    the provided focus_half_width
    The focus_half_width can be a unique value applied to all or a list of
    values of the same length as focus.

    focus is then return as a (n, 2) array where:
        each line gives a central wavelength and halfwidth of interest

    """
    if focus in [None, False]:
        return False

    # Check focus and transform to array of floats
    lc0 = [type(focus) in [str] + _LTYPES,
           type(focus) in [list, tuple, np.ndarray]]
    if not any(lc0):
        msg = _dvalid_checkfocus_errmsg(focus, focus_half_width,
                                        lines_keys)
        raise Exception(msg)
    if lc0[0] is True:
        focus = [focus]
    for ii in range(len(focus)):
        if focus[ii] not in lines_keys and type(focus[ii]) not in _LTYPES:
            msg = _dvalid_checkfocus_errmsg(focus, focus_half_width,
                                            lines_keys)
            raise Exception(msg)
    focus = np.array([lines_lamb[(lines_keys == ff).nonzero()[0][0]]
                      if ff in lines_keys else ff for ff in focus])

    # Check focus_half_width and transform to array of floats
    if focus_half_width is None:
        focus_half_width = (np.max(lines_lamb) - np.min(lines_lamb))/20
    lc0 = [type(focus_half_width) in _LTYPES,
           (type(focus_half_width) in [list, tuple, np.ndarray]
            and len(focus_half_width) == focus.size
            and all([type(fhw) in _LTYPES for fhw in focus_half_width]))]
    if not any(lc0):
        msg = _dvalid_checkfocus_errmsg(focus, focus_half_width,
                                        lines_keys)
        raise Exception(msg)
    if lc0[0] is True:
        focus_half_width = np.full((focus.size,), focus_half_width)
    return np.array([focus, np.r_[focus_half_width]]).T


def fit12d_dvalid(data=None, lamb=None, phi=None,
                  indok=None, binning=None,
                  valid_nsigma=None, valid_fraction=None,
                  focus=None, focus_half_width=None,
                  lines_keys=None, lines_lamb=None, dphimin=None,
                  nbs=None, deg=None, knots_mult=None, nknotsperbs=None,
                  return_fract=None):
    """ Return a dict of valid time steps and phi indices

    data points are considered valid if there signal is sufficient:
        np.sqrt(data) >= valid_nsigma

    data is supposed to be provided in counts (or photons).. TBC!!!

    """

    # Check inputs
    if valid_nsigma is None:
        valid_nsigma = _VALID_NSIGMA
    if valid_fraction is None:
        valid_fraction = _VALID_FRACTION
    if binning is None:
        binning = False
    if dphimin is None:
        dphimin = 0.
    if return_fract is None:
        return_fract = False
    data2d = data.ndim == 3
    nspect = data.shape[0]

    focus = _dvalid_checkfocus(focus,
                               focus_half_width=focus_half_width,
                               lines_keys=lines_keys,
                               lines_lamb=lines_lamb)

    # Get indices of pts with enough signal
    ind = np.zeros(data.shape, dtype=bool)
    if indok is None:
        isafe = (~np.isnan(data))
        isafe[isafe] = data[isafe] >= 0.
        # Ok with and w/o binning if data provided as counts / photons
        # and binning was done by sum (and not mean)
        ind[isafe] = np.sqrt(data[isafe]) > valid_nsigma
    else:
        ind[:, indok] = np.sqrt(data[:, indok]) > valid_nsigma

    # Derive indt and optionally dphi and indknots
    indbs, dphi = False, False
    if focus is not False:
        lambok = np.rollaxis(
            np.array([np.abs(lamb - ff[0]) < ff[1] for ff in focus]),
            0, lamb.ndim+1)
        indall = ind[..., None] & lambok[None, ...]

    if data2d is True:
        # Make sure there are at least deg + 2 different phi
        deltaphi = np.max(np.diff(knots_mult))
        # Code ok with and without binning :-)
        if focus is False:
            fract = np.full((nspect, nbs), np.nan)
            for ii in range(nbs):
                iphi = ((phi >= knots_mult[ii])
                        & (phi < knots_mult[ii+nknotsperbs-1]))
                fract[:, ii] = (np.sum(np.sum(ind & iphi[None, ...],
                                              axis=-1), axis=-1)
                                / np.sum(iphi))
            indbs = fract > valid_fraction
        else:
            fract = np.full((nspect, nbs, len(focus)), np.nan)
            for ii in range(nbs):
                iphi = ((phi >= knots_mult[ii])
                        & (phi < knots_mult[ii+nknotsperbs-1]))
                fract[:, ii, :] = (
                    np.sum(np.sum(indall & iphi[None, ..., None],
                                  axis=1), axis=1)
                    / np.sum(np.sum(iphi[..., None] & lambok,
                                    axis=0), axis=0))
            indbs = np.all(fract > valid_fraction, axis=2)
        indt = np.any(indbs, axis=1)
        dphi = deltaphi*(deg + indbs[:, deg:-deg].sum(axis=1))

    else:
        # 1d spectra
        if focus is False:
            fract = ind.sum(axis=-1) / ind.shape[1]
            indt = fract > valid_fraction
        else:
            fract = np.sum(indall, axis=1) / lambok.sum(axis=0)[None, :]
            indt = np.all(fract > valid_fraction, axis=1)

    # Optional debug
    if focus is not False and False:
        indt_debug, ifocus = 40, 1
        if data2d is True:
            indall2 = indall.astype(int)
            indall2[:, lambok] = 1
            indall2[ind[..., None] & lambok[None, ...]] = 2
            plt.figure();
            plt.imshow(indall2[indt_debug, :, :, ifocus].T, origin='lower');
        else:
            plt.figure();
            plt.plot(lamb[~indall[indt_debug, :, ifocus]],
                     data[indt_debug, ~indall[indt_debug, :, ifocus]], '.k',
                     lamb[indall[indt_debug, :, ifocus]],
                     data[indt_debug, indall[indt_debug, :, ifocus]], '.r');
            plt.axvline(focus[ifocus, 0], ls='--', c='k');

    # return
    dvalid = {'indt': indt, 'dphi': dphi, 'indbs': indbs, 'ind': ind,
              'focus': focus, 'valid_fraction': valid_fraction,
              'valid_nsigma': valid_nsigma}
    if return_fract is True:
        dvalid['fract'] = fract
    return dvalid


###########################################################
###########################################################
#
#           dlines dict (lines vs domain)
#
###########################################################
###########################################################


def _checkformat_dlines(dlines=None, domain=None):
    if dlines is None:
        dlines = False
    c0 = (isinstance(dlines, dict)
          and all([(isinstance(k0, str)
                    and isinstance(v0, dict)
                    and 'lambda0' in v0.keys())
                   for k0, v0 in dlines.items()]))
    if c0 is not True:
        msg = ("Arg dlines must be a dict of the form:\n"
               + "\t{'line0': {'lambda0': float},\n"
               + "\t 'line1': {'lambda0': float},\n"
               + "\t  ...\n"
               + "\t 'lineN': {'lambda0': float}}\n"
               + "  You provided: {}".format(dlines))
        raise Exception(msg)

    # Select relevant lines (keys, lamb)
    lines_keys = np.array([k0 for k0 in dlines.keys()])
    lines_lamb = np.array([dlines[k0]['lambda0'] for k0 in lines_keys])
    if domain not in [None, False]:
        ind = ((lines_lamb >= domain['lamb']['minmax'][0])
               & (lines_lamb <= domain['lamb']['minmax'][1]))
        lines_keys = lines_keys[ind]
        lines_lamb = lines_lamb[ind]
    inds = np.argsort(lines_lamb)
    lines_keys, lines_lamb = lines_keys[inds], lines_lamb[inds]
    nlines = lines_lamb.size
    return dlines, lines_keys, lines_lamb


###########################################################
###########################################################
#
#           dinput dict (lines + spectral constraints)
#
###########################################################
###########################################################


def fit1d_dinput(
    dlines=None, dconstraints=None, dprepare=None,
    data=None, lamb=None, mask=None,
    domain=None, pos=None, subset=None,
    same_spectrum=None, nspect=None, same_spectrum_dlamb=None,
    focus=None, valid_fraction=None, valid_nsigma=None, focus_half_width=None,
    valid_return_fract=None,
    dscales=None, dx0=None, dbounds=None,
    defconst=_DCONSTRAINTS):
    """ Check and format a dict of inputs to be fed to fit1d()

    This dict will contain all information relevant for solving the fit:
        - dlines: dict of lines (with 'lambda0': wavelength at rest)
        - lamb: vector of wavelength of the experimental spectrum
        - data: experimental spectrum, possibly 2d (time-varying)
        - dconstraints: dict of constraints on lines (amp, width, shift)
        - pos: bool, consider only positive data (False => replace <0 with nan)
        - domain:
        - mask: 
        - subset:
        - same_spectrum: 
        - focus: 

    """

    # ------------------------
    # Check / format dprepare
    # ------------------------
    if dprepare is None:
        dprepare = multigausfit1d_from_dlines_prepare(
            data=data, lamb=lamb,
            mask=mask, domain=domain,
            pos=pos, subset=subset)

    # ------------------------
    # Check / format dlines
    # ------------------------
    dlines, lines_keys, lines_lamb = _checkformat_dlines(
        dlines=dlines,
        domain=dprepare['domain'],
    )
    nlines = lines_lamb.size

    # Check same_spectrum
    if same_spectrum is None:
        same_spectrum = _SAME_SPECTRUM
    if same_spectrum is True:
        if type(nspect) not in [int, np.int]:
            msg = "Please provide nspect if same_spectrum = True"
            raise Exception(msg)
        if same_spectrum_dlamb is None:
            same_spectrum_dlamb = min(
                2*np.diff(dprepare['domain']['lamb']['minmax']),
                dprepare['domain']['lamb']['minmax'][0],
            )

    # ------------------------
    # Check / format dconstraints
    # ------------------------

    dconstraints = _checkformat_dconstraints(
        dconstraints=dconstraints, defconst=defconst,
    )
    dinput = {}

    # ------------------------
    # Check / format double
    # ------------------------
    _dconstraints_double(dinput, dconstraints, defconst=defconst)

    # ------------------------
    # Check / format width, shift, amp (groups with posssible ratio)
    # ------------------------
    for k0 in ['amp', 'width', 'shift']:
        dinput[k0] = _width_shift_amp(dconstraints.get(k0, defconst[k0]),
                                      keys=lines_keys, nlines=nlines,
                                      dlines=dlines, k0=k0)

    # ------------------------
    # add mz, symb, ION, keys, lamb
    # ------------------------
    mz = np.array([dlines[k0].get('m', np.nan) for k0 in lines_keys])
    symb = np.array([dlines[k0].get('symbol', k0) for k0 in lines_keys])
    ion = np.array([dlines[k0].get('ION', '?') for k0 in lines_keys])

    # ------------------------
    # same_spectrum
    # ------------------------
    if same_spectrum is True:
        keysadd = np.array([[kk+'_bis{:04.0f}'.format(ii) for kk in keys]
                            for ii in range(1, nspect)]).ravel()
        lines_lamb = (same_spectrum_dlamb
                      *np.arange(0, nspect)[:, None]
                      + lines_lamb[None, :])
        keys = np.r_[keys, keysadd]

        for k0 in ['amp', 'width', 'shift']:
            # Add other lines to original group
            keyk = dinput[k0]['keys']
            offset = np.tile(dinput[k0]['offset'], nspect)
            if k0 == 'shift':
                ind = np.tile(dinput[k0]['ind'], (1, nspect))
                coefs = (dinput[k0]['coefs']
                         * lines_lamb[0, :] / lines_lamb).ravel()
            else:
                coefs = np.tile(dinput[k0]['coefs'], nspect)
                keysadd = np.array([[kk+'_bis{:04.0f}'.format(ii)
                                     for kk in keyk]
                                    for ii in range(1, nspect)]).ravel()
                ind = np.zeros((keyk.size*nspect, nlines*nspect))
                for ii in range(nspect):
                    i0, i1 = ii*keyk.size, (ii+1)*keyk.size
                    j0, j1 = ii*nlines, (ii+1)*nlines
                    ind[i0:i1, j0:j1] = dinput[k0]['ind']
                keyk = np.r_[keyk, keysadd]
            dinput[k0]['keys'] = keyk
            dinput[k0]['ind'] = ind
            dinput[k0]['coefs'] = coefs
            dinput[k0]['offset'] = offset
        nlines *= nspect
        lines_lamb = lines_lamb.ravel()

        # update mz, symb, ion
        mz = np.tile(mz, nspect)
        symb = np.tile(symb, nspect)
        ion = np.tile(ion, nspect)

    # ------------------------
    # add lines and properties
    # ------------------------
    dinput['keys'] = lines_keys
    dinput['lines'] = lines_lamb
    dinput['nlines'] = nlines

    dinput['mz'] = mz
    dinput['symb'] = symb
    dinput['ion'] = ion

    dinput['same_spectrum'] = same_spectrum
    if same_spectrum is True:
        dinput['same_spectrum_nspect'] = nspect
        dinput['same_spectrum_dlamb'] = same_spectrum_dlamb
    else:
        dinput['same_spectrum_nspect'] = False
        dinput['same_spectrum_dlamb'] = False

    # ------------------------
    # S/N threshold indices
    # ------------------------
    dinput['valid'] = fit12d_dvalid(
        data=dprepare['data'],
        lamb=dprepare['lamb'],
        indok=dprepare['indok'],
        valid_nsigma=valid_nsigma,
        valid_fraction=valid_fraction,
        focus=focus, focus_half_width=focus_half_width,
        lines_keys=lines_keys, lines_lamb=lines_lamb,
        return_fract=valid_return_fract)

    # Update with dprepare
    dinput['dprepare'] = dict(dprepare)

    # Add dind
    dinput['dind'] = multigausfit1d_from_dlines_ind(dinput)

    # Add dscales, dx0 and dbounds
    dinput['dscales'] = fit12d_dscales(dscales=dscales,
                                       dinput=dinput)
    dinput['dx0'] = fit12d_dx0(dx0=dx0, dinput=dinput)       # TBF
    # dinput['dbounds'] = fit12d_dbounds()
    return dinput


def fit2d_dinput(
    dlines=None, dconstraints=None, dprepare=None,
    deg=None, nbsplines=None, knots=None,
    data=None, lamb=None, phi=None, mask=None,
    domain=None, pos=None, subset=None, binning=None, cent_fraction=None,
    focus=None, valid_fraction=None, valid_nsigma=None, focus_half_width=None,
    valid_return_fract=None,
    dscales=None, dx0=None, dbounds=None,
    nxi=None, nxj=None,
    lphi=None, lphi_tol=None,
    defconst=_DCONSTRAINTS):

    # ------------------------
    # Check / format dprepare
    # ------------------------
    if dprepare is None:
        dprepare = multigausfit2d_from_dlines_prepare(
            data=data, lamb=lamb, phi=phi,
            mask=mask, domain=domain,
            pos=pos, subset=subset, binning=binning,
            nbsplines=nbsplines, nxi=nxi, nxj=nxj,
            lphi=None, lphi_tol=None)

    # ------------------------
    # Check / format dlines
    # ------------------------
    dlines, lines_keys, lines_lamb = _checkformat_dlines(
        dlines=dlines,
        domain=dprepare['domain'])
    nlines = lines_lamb.size

    # ------------------------
    # Check / format dconstraints
    # ------------------------

    dconstraints = _checkformat_dconstraints(dconstraints=dconstraints,
                                             defconst=defconst)
    dinput = {}

    # ------------------------
    # Check / format symmetry
    # ------------------------
    _dconstraints_symmetry(dinput, symmetry=dconstraints.get('symmetry'),
                           dataphi1d=dprepare.get('dataphi1d'),
                           phi1d=dprepare.get('phi1d'),
                           cent_fraction=cent_fraction, defconst=defconst)

    # ------------------------
    # Check / format double (spectral line doubling)
    # ------------------------
    _dconstraints_double(dinput, dconstraints, defconst=defconst)

    # ------------------------
    # Check / format width, shift, amp (groups with posssible ratio)
    # ------------------------
    for k0 in ['amp', 'width', 'shift']:
        dinput[k0] = _width_shift_amp(dconstraints.get(k0, defconst[k0]),
                                      keys=lines_keys, nlines=nlines,
                                      dlines=dlines, k0=k0)

    # ------------------------
    # add mz, symb, ION, keys, lamb
    # ------------------------
    mz = np.array([dlines[k0].get('m', np.nan) for k0 in lines_keys])
    symb = np.array([dlines[k0].get('symbol', k0) for k0 in lines_keys])
    ion = np.array([dlines[k0].get('ION', '?') for k0 in lines_keys])

    dinput['keys'] = lines_keys
    dinput['lines'] = lines_lamb
    dinput['nlines'] = nlines

    dinput['mz'] = mz
    dinput['symb'] = symb
    dinput['ion'] = ion

    # ------------------------
    # Get dict of bsplines
    # ------------------------
    dinput.update(multigausfit2d_from_dlines_dbsplines(
        knots=knots, deg=deg, nbsplines=nbsplines,
        phimin=dprepare['domain']['phi']['minmax'][0],
        phimax=dprepare['domain']['phi']['minmax'][1],
        symmetryaxis=dinput.get('symmetry_axis')))

    # ------------------------
    # S/N threshold indices
    # ------------------------
    dinput['valid'] = fit12d_dvalid(
        data=dprepare['data'],
        lamb=dprepare['lamb'],
        phi=dprepare['phi'],
        binning=dprepare['binning'],
        indok=dprepare['indok'],
        valid_nsigma=valid_nsigma,
        valid_fraction=valid_fraction,
        focus=focus, focus_half_width=focus_half_width,
        lines_keys=lines_keys, lines_lamb=lines_lamb,
        nbs=dinput['nbs'],
        deg=dinput['deg'],
        knots_mult=dinput['knots_mult'],
        nknotsperbs=dinput['nknotsperbs'],
        return_fract=valid_return_fract)

    # Update with dprepare
    dinput['dprepare'] = dict(dprepare)

    # Add dind
    dinput['dind'] = multigausfit2d_from_dlines_ind(dinput)

    # Add dscales, dx0 and dbounds
    dinput['dscales'] = fit12d_dscales(dscales=dscales,
                                       dinput=dinput)
    # dinput['dx0'] = fit12d_dx0(dinput=dinput)
    # dinput['dbounds'] = fit12d_dbounds()
    return dinput


###########################################################
###########################################################
#
#           dind dict (indices storing for fast access)
#
###########################################################
###########################################################


def multigausfit1d_from_dlines_ind(dinput=None):
    """ Return the indices of quantities in x to compute y """

    # indices
    # General shape: [bck, amp, widths, shifts]
    # If double [..., double_shift, double_ratio]
    # Except for bck, all indices should render nlines (2*nlines if double)
    dind = {'bck': {'x': np.r_[0]},
            'dshift': None,
            'dratio': None}
    nn = dind['bck']['x'].size
    inddratio, inddshift = None, None
    for k0 in ['amp', 'width', 'shift']:
        ind = dinput[k0]['ind']
        lnl = np.sum(ind, axis=1).astype(int)
        dind[k0] = {'x': nn + np.arange(0, ind.shape[0]),
                    'lines': nn + np.argmax(ind, axis=0),
                    'jac': [tuple(ind[ii, :].nonzero()[0])
                            for ii in range(dinput[k0]['ind'].shape[0])]}
        nn += dind[k0]['x'].size

    sizex = dind['shift']['x'][-1] + 1
    indx = np.r_[dind['bck']['x'], dind['amp']['x'],
                 dind['width']['x'], dind['shift']['x']]
    assert np.all(np.arange(0, sizex) == indx)

    # check if double
    if dinput['double'] is True:
        dind['dshift'] = {'x': -2}
        dind['dratio'] = {'x': -1}
        sizex += 2
    elif isinstance(dinput['double'], dict):
        if dinput['double'].get('dshift') is None:
            dind['dshift'] = {'x': -1}
            sizex += 1
        elif dinput['double'].get('dratio') is None:
            dind['dratio'] = {'x': -1}
            sizex += 1

    dind['sizex'] = sizex
    dind['nbck'] = 1
    # dind['shapey1'] = dind['bck']['x'].size + dinput['nlines']

    # Ref line for amp (for dscales)
    amp_x0 = np.zeros((dinput['amp']['ind'].shape[0],), dtype=int)
    for ii in range(dinput['amp']['ind'].shape[0]):
        indi = dinput['amp']['ind'][ii, :].nonzero()[0]
        amp_x0[ii] = indi[np.argmin(np.abs(dinput['amp']['coefs'][indi]-1.))]
    dind['amp_x0'] = amp_x0
    return dind


def multigausfit2d_from_dlines_ind(dinput=None):
    """ Return the indices of quantities in x to compute y """

    # indices
    # General shape: [bck, amp, widths, shifts]
    # If double [..., double_shift, double_ratio]
    # Except for bck, all indices should render nlines (2*nlines if double)
    nbs = dinput['nbs']
    dind = {'bck': {'x': np.arange(0, nbs)},
            'dshift': None,
            'dratio': None}
    nn = dind['bck']['x'].size
    inddratio, inddshift = None, None
    for k0 in ['amp', 'width', 'shift']:
        # l0bs0, l0bs1, ..., l0bsN, l1bs0, ...., lnbsN
        ind = dinput[k0]['ind']
        lnl = np.sum(ind, axis=1).astype(int)
        dind[k0] = {'x': (nn
                          + nbs*np.arange(0, ind.shape[0])[None, :]
                          + np.arange(0, nbs)[:, None]),
                    'lines': (nn
                              + nbs*np.argmax(ind, axis=0)[None, :]
                              + np.arange(0, nbs)[:, None]),
                    # TBF
                    'jac': [ind[ii, :].nonzero()[0]
                            for ii in range(ind.shape[0])]}
        nn += dind[k0]['x'].size

    sizex = dind['shift']['x'][-1, -1] + 1
    indx = np.r_[dind['bck']['x'], dind['amp']['x'].T.ravel(),
                 dind['width']['x'].T.ravel(), dind['shift']['x'].T.ravel()]
    assert np.allclose(np.arange(0, sizex), indx)

    # check if double
    if dinput['double'] is True:
        dind['dshift'] = {'x': -2}
        dind['dratio'] = {'x': -1}
        sizex += 2
    elif isinstance(dinput['double'], dict):
        if dinput['double'].get('dshift') is None:
            dind['dshift'] = {'x': -1}
            sizex += 1
        elif dinput['double'].get('dratio') is None:
            dind['dratio'] = {'x': -1}
            sizex += 1

    dind['sizex'] = sizex
    dind['nbck'] = 1

    # Ref line for amp (for x0)
    # TBC !!!
    amp_x0 = np.zeros((dinput['amp']['ind'].shape[0],), dtype=int)
    for ii in range(dinput['amp']['ind'].shape[0]):
        indi = dinput['amp']['ind'][ii, :].nonzero()[0]
        amp_x0[ii] = indi[np.argmin(np.abs(dinput['amp']['coefs'][indi]-1.))]
    dind['amp_x0'] = amp_x0

    # Make bsplines selections easy
    # if dinput['valid']['dphi'] is not False:
        # dind['bs']['x'] = 
        # import pdb; pdb.set_trace()     # DB
        # pass

    return dind


###########################################################
###########################################################
#
#           scales (for variables scaling)
#
###########################################################
###########################################################


def _fit12d_checkformat_dscalesx0(din=None, dinput=None, name=None):
    lkconst = ['dratio', 'dshift']
    lk = ['bck']
    lkdict = ['amp', 'width', 'shift']
    c0 = din is None
    c1 = (
        isinstance(din, dict)
        and all([
            (k0 in lkconst and type(v0) in _LTYPES)
            or (
                k0 in lk and type(v0) in _LTYPES + [np.ndarray])
                or (
                    k0 in lkdict
                    and isinstance(v0, dict)
                    and all([
                        k1 in dinput[k0]['keys']
                        and type(v1) in _LTYPES + [np.ndarray]
                        for k1, v1 in v0.items()
                    ])
                )
            for k0, v0 in din.items()
        ])
    )
    if c0 is True:
        din = {}
    elif not c1:
        msg = ("Arg {} must be a dict of the form:\n".format(name)
               + "\t- {}\n".format(dict.fromkeys(lk, 1.))
               + "\t- provided: {}".format(din))
        raise Exception(msg)
    return din


def _fit12d_filldef_dscalesx0_dict(
    din=None, din_name=None, key=None, vref=None, nspect=None, dinput=None,
):

    # Check vref
    if vref is not None:
        if type(vref) not in _LTYPES and len(vref) != nspect:
            msg = (
                "Non-conform vref for "
                + "{}['{}']\n".format(din_name, key)
                + "\t- expected: float or np.ndarray (size {})".format(nspect)
                + "\t- provided: {}".format(vref)
            )
            raise Exception(msgi)
        if type(vref) in _LTYPES:
            vref = np.full((nspect,), vref)

    # check din[key]
    if din.get(key) is None:
        assert vref is not None
        din[key] = {k0: vref for k0 in dinput[key]['keys']}

    else:
        for k0 in dinput[key]['keys']:
            if din[key].get(k0) is None:
                din[key][k0] = vref
            elif type(din[key][k0]) in _LTYPES:
                din[key][k0] = np.full((nspect,), din[key][k0])
            elif din[key][k0].shape != (nspect,):
                msg = (
                    "Non-conform value for "
                    + "{}['{}']['{}']\n".format(din_name, key, k0)
                    + "\t- expected: float or array (size {})".format(nspect)
                    + "\t- provided: {}".format(din[key][k0])
                )
                raise Exception(msg)
    return din


def _fit12d_filldef_dscalesx0_float(
    din=None, din_name=None, key=None, vref=None, nspect=None,
):
    if dx0.get(key) is None:
        if type(vref) is _LTYPES:
            din[key] = np.full((nspect,), vref)
        elif vref.shape == nspect
            din[key] = vref
        else:
            msg = (
                "Non-conform vref for {}['{}']\n".format(din_name, key)
                + "\t- expected: float or np.ndarray (size {})".format(nspect)
                + "\t- provided: {}".format(vref)
            )
            raise Exception(msg)
    else:
        if type(dx0[key]) in _LTYPES:
            din[key] = np.full((nspect,), din[key])
        elif din[key].shape != (nspect,):
            msg = (
                "Non-conform vref for {}['{}']\n".format(din_name, key)
                + "\t- expected: float or np.ndarray (size {})".format(nspect)
                + "\t- provided: {}".format(din[key])
            )
            raise Exception(msg)
    return din


def fit12d_dscales(dscales=None,
                   dinput=None):

    # --------------
    # Input checks
    dscales = _fit12d_checkformat_dscalesx0(
        din=dscales, dinput=dinput, name='dscales',
    )

    data = dinput['dprepare']['data']
    lamb = dinput['dprepare']['lamb']
    nspect = data.shape[0]

    # --------------
    # 2d spectrum = 1d spectrum + vert. profile
    data2d = data.ndim == 3
    if data2d is True:
        phi = dinput['dprepare']['phi']
        if dinput['dprepare']['binning'] is False:
            lambbins = np.linspace(
                dinput['dprepare']['domain']['lamb']['minmax'][0],
                dinput['dprepare']['domain']['lamb']['minmax'][1],
                dinput['dprepare']['nxi']-1)
            phibins = np.linspace(
                dinput['dprepare']['domain']['phi']['minmax'][0],
                dinput['dprepare']['domain']['phi']['minmax'][1],
                dinput['dprepare']['nxj']-1)
            datavert = scpstats.binned_statistic(
                phi[dinput['dprepare']['indok']],
                data[:, dinput['dprepare']['indok']],
                statistic='mean', bins=phibins, range=None)[0]
            data = scpstats.binned_statistic(
                lamb[dinput['dprepare']['indok']],
                data[:, dinput['dprepare']['indok']],
                statistic='mean', bins=lambbins, range=None)[0]
            lamb = 0.5*(lambbins[1:] + lambbins[:-1])
            phi = 0.5*(phibins[1:] + phibins[:-1])
        else:
            datavert = np.nanmean(data, axis=1)
            data = np.nanmean(data, axis=2)
            lamb = lamb[:, 0]
            phi = phi[0, :]

        # bsplines modulation of bck and amp, if relevant
        # fit bsplines on datavert (vertical profile)
        # to modulate scales (bck and amp)

        dscales['bs'] = np.full((nspect, dinput['nbs']), np.nan)
        for ii in dinput['valid']['indt'].nonzero()[0]:
            indnonan = ~np.isnan(datavert[ii, :])
            bs = scpinterp.LSQUnivariateSpline(
                phi[indnonan], datavert[ii, indnonan],
                dinput['knots'][1:-1],
                k=dinput['deg'],
                bbox=dinput['knots'][np.r_[0,-1]],
                ext=0)
            dscales['bs'][ii, :] = bs.get_coeffs()
        # Normalize to avoid double-amplification when amp*bs
        corr = np.max(dscales['bs'][dinput['valid']['indt'], :],
                      axis=1)[:, None]
        dscales['bs'][dinput['valid']['indt'], :] /= corr

    # --------------
    # Default values for filling missing fields
    Dlamb = np.diff(dinput['dprepare']['domain']['lamb']['minmax'])
    lambm = dinput['dprepare']['domain']['lamb']['minmax'][0]

    # bck
    bckref = None
    if dscales.get('bck') is None:
        indbck = data < np.nanmean(data, axis=1)[:, None]
        bckref = np.array(np.ma.masked_where(
            indbck, data,
        ).mean(axis=1))
    dscales = _fit12d_filldef_dscalesx0_float(
        din=dscales, din_name='dscales', key='bck', vref=bckref, nspect=nspect,
    )

    # amp
    dscales['amp'] = dscales.get('amp', dict.fromkeys(dinput['amp']['keys']))
    for ii, ij in enumerate(dinput['dind']['amp_x0']):
        key = dinput['amp']['keys'][ii]
        if dscales['amp'].get(key) is None:
            indi = np.abs(lamb-dinput['lines'][ij]) < Dlamb/20.
            dscales['amp'][key] = np.nanmean(data[:, indi], axis=1)
        else:
            if type(dscales['amp'][key]) in _LTYPES:
                dscales['amp'][key] = np.full((nspect,), dscales['amp'][key])
            else:
                assert dscales['amp'][key].shape == (nspect,)

    # width
    if dinput.get('same_spectrum') is True:
        lambm2 = (lambm
                 + dinput['same_spectrum_dlamb']
                 * np.arange(0, dinput['same_spectrum_nspect']))
        nw0 = iwx.size / dinput['same_spectrum_nspect']
        lambmw = np.repeat(lambm2, nw0)
        widthref = (Dlamb/(20*lambmw))**2
    else:
        widthref = (Dlamb/(20*lambm))**2

    dscales = _fit12d_filldef_dscalesx0_dict(
        din=dscales, din_name='dscales', key='width', vref=widthref,
        nspect=nspect, dinput=dinput,
    )

    # shift
    shiftref = Dlamb/(50*lambm)
    dscales = _fit12d_filldef_dscalesx0_dict(
        din=dscales, din_name='dscales', key='shift', vref=shiftref,
        nspect=nspect, dinput=dinput,
    )

    # Double
    if dinput['double'] is not False:
        dratio = 1.
        dshift = float(Dlamb/(50*lambm))
        if dinput['double'] is True:
            pass
        else:
            if dinput['double'].get('dratio') is not None:
                dratio = dinput['double']['dratio']
            if dinput['double'].get('dshift') is not None:
                dratio = dinput['double']['dshift']
        dscales = _fit12d_filldef_dscalesx0_float(
            din=dscales, din_name='dscales', key='dratio',
            vref=dratio, nspect=nspect,
        )
        dscales = _fit12d_filldef_dscalesx0_float(
            din=dscales, din_name='dscales', key='dshift',
            vref=dshift, nspect=nspect,
        )
    return dscales


def multigausfit1d_from_dlines_scale(data, lamb,
                                     scales=None, dscales=None,
                                     domain=None, dinput=None,
                                     dind=None, nspect=None):
    if dscales is None:
        dscales = False

    if scales is None:
        scales = np.full((nspect, dind['sizex']), np.nan)
        Dlamb = domain['lamb']['minmax'][1] - domain['lamb']['minmax'][0]
        lambm = domain['lamb']['minmax'][0]
        ibckx, iax = dind['bck']['x'], dind['amp']['x']
        iwx, isx = dind['width']['x'], dind['shift']['x']

        # bck
        indbck = data < np.nanmean(data, axis=1)[:, None]
        scales[:, ibckx[0]] = np.ma.masked_where(indbck, data).mean(axis=1)

        # amp
        for ii, ij in enumerate(dind['amp_x0']):
            indi = np.abs(lamb-dinput['lines'][ij]) < Dlamb/20.
            scales[:, iax[ii]] = np.nanmean(data[:, indi], axis=1)

        # width and shift
        if dinput['same_spectrum'] is True:
            lambm2 = (lambm
                     + dinput['same_spectrum_dlamb']
                     * np.arange(0, dinput['same_spectrum_nspect']))
            nw0 = iwx.size / dinput['same_spectrum_nspect']
            lambmw = np.repeat(lambm2, nw0)
            scales[:, iwx] = (Dlamb/(20*lambmw))**2
        else:
            scales[:, iwx] = (Dlamb/(20*lambm))**2
        scales[:, isx] = Dlamb/(50*lambm)

        # Double
        if dinput['double'] is not False:
            if dinput['double'] is True:
                scales[:, dind['dratio']['x']] = 1.
                scales[:, dind['dshift']['x']] = Dlamb/(50*lambm)
            else:
                if dinput['double'].get('dratio') is None:
                    scales[:, dind['dratio']['x']] = 1.
                if dinput['double'].get('dshift') is None:
                    scales[:, dind['dshift']['x']] = Dlamb/(50*lambm)

    # check and return
    assert scales.ndim in [1, 2]
    if scales.ndim == 1:
        scales = np.tile(scales, (nspect, scales.size))
    assert scales.shape == (nspect, dind['sizex'])

    # Adjust with user-provided dscales
    if dscales is not False:
        lk = ['bck', 'amp', 'width', 'shift', 'dratio', 'dshift']
        c0 = (isinstance(dscales, dict)
              and all([type(dscales.get(ss, 1.)) in _LTYPES for ss in lk]))
        if not c0:
            msg = ("Arg dscales must be a dict of the form (1. is default):\n"
                   + "\t- {}\n".format(dict.fromkeys(lk, 1.))
                   + "\t- provided: {}".format(dscales))
            raise Exception(msg)

        for kk in lk:
            scales[:, dind[kk]['x']] *= dscales.get(kk, 1.)
    return scales


def multigausfit2d_from_dlines_scale(data, lamb, phi,
                                     scales=None, dscales=None,
                                     domain=None, dinput=None,
                                     dind=None, nspect=None):
    if dscales is None:
        dscales = False

    if scales is None:
        scales = np.full((nspect, dind['sizex']), np.nan)
        Dphi = domain['phi']['minmax'][1] - domain['phi']['minmax'][0]
        Dlamb = domain['lamb']['minmax'][1] - domain['lamb']['minmax'][0]
        lambm = domain['lamb']['minmax'][0]
        ibckx, iax = dind['bck']['x'], dind['amp']['x']
        iwx, isx = dind['width']['x'].ravel(), dind['shift']['x'].ravel()

        # Perform by sector
        nbs, nlines = dinput['nbs'], dinput['nlines']
        na = dinput['amp']['ind'].shape[0]
        for ii in range(nbs):
            ind = np.abs(phi-dinput['ptsx0'][ii]) < Dphi/20.

            # bck
            for jj in range(nspect):
                indbck = data[jj, ind] < np.nanmean(data[jj, ind])
                scales[jj, ibckx[ii]] = np.nanmean(data[jj, ind][indbck])

            # amp
            for jj in range(na):
                indl = dind['amp_x0'][jj]
                indlamb = np.abs(lamb-dinput['lines'][indl]) < Dlamb/20.
                indj = ind & indlamb
                if not np.any(indj):
                    lamb0 = dinput['lines'][indl]
                    msg = ("All nan in region scanned for scale:\n"
                           + "\t- amp[{}]\n".format(jj)
                           + "\t- bspline[{}]\n".format(ii)
                           + "\t- phi approx {}\n".format(dinput['ptsx0'][ii])
                           + "\t- lamb approx {}".format(lamb0))
                    plt.figure()
                    plt.scatter(lamb, phi, s=6, c='k', marker='.')
                    plt.scatter(lamb[ind], phi[ind], s=6, c='r', marker='.')
                    plt.scatter(lamb[indlamb], phi[indlamb],
                                s=6, c='b', marker='.');
                    plt.gca().set_xlim(domain['lamb']['minmax'])
                    plt.gca().set_ylim(domain['phi']['minmax'])
                    raise Exception(msg)
                scales[:, iax[ii, jj]] = np.nanmean(data[:, indj], axis=1)

        # width and shift
        scales[:, iwx] = (Dlamb/(20*lambm))**2
        scales[:, isx] = Dlamb/(50*lambm)

        # double
        if dinput['double'] is not False:
            if dinput['double'] is True:
                scales[:, dind['dratio']['x']] = 1.
                scales[:, dind['dshift']['x']] = Dlamb/(50*lambm)
            else:
                if dinput['double'].get('dratio') is None:
                    scales[:, dind['dratio']['x']] = 1.
                if dinput['double'].get('dshift') is None:
                    scales[:, dind['dshift']['x']] = Dlamb/(50*lambm)

    # check and return
    assert scales.ndim in [1, 2]
    if scales.ndim == 1:
        scales = np.tile(scales, (nspect, scales.size))
    assert scales.shape == (nspect, dind['sizex'])

    # Adjust with user-provided dscales
    if dscales is not False:
        lk = ['bck', 'amp', 'width', 'shift', 'dratio', 'dshift']
        c0 = (isinstance(dscales, dict)
              and all([type(dscales.get(ss, 1.)) in _LTYPES for ss in lk]))
        if not c0:
            msg = ("Arg dscales must be a dict of the form (1. is default):\n"
                   + "\t- {}\n".format(dict.fromkeys(lk, 1.))
                   + "\t- provided: {}".format(dscales))
            raise Exception(msg)

        for kk in lk:
            scales[:, dind[kk]['x']] *= dscales.get(kk, 1.)
    return scales


###########################################################
###########################################################
#
#           x0 (initial guess)
#
###########################################################
###########################################################


def fit12d_dx0(dx0=None, dinput=None):

    # --------------
    # Input checks
    dx0 = _fit12d_checkformat_dscalesx0(
        din=dx0, dinput=dinput, name='dx0',
    )

    data = dinput['dprepare']['data']
    lamb = dinput['dprepare']['lamb']
    nspect = data.shape[0]

    # --------------
    # 2d spectrum = 1d spectrum + vert. profile
    data2d = data.ndim == 3
    # if data2d is True:
        # phi = dinput['dprepare']['phi']
        # if dinput['dprepare']['binning'] is False:
            # lambbins = np.linspace(
                # dinput['dprepare']['domain']['lamb']['minmax'][0],
                # dinput['dprepare']['domain']['lamb']['minmax'][1],
                # dinput['dprepare']['nxi']-1)
            # phibins = np.linspace(
                # dinput['dprepare']['domain']['phi']['minmax'][0],
                # dinput['dprepare']['domain']['phi']['minmax'][1],
                # dinput['dprepare']['nxj']-1)
            # datavert = scpstats.binned_statistic(
                # phi[dinput['dprepare']['indok']],
                # data[:, dinput['dprepare']['indok']],
                # statistic='mean', bins=phibins, range=None)[0]
            # data = scpstats.binned_statistic(
                # lamb[dinput['dprepare']['indok']],
                # data[:, dinput['dprepare']['indok']],
                # statistic='mean', bins=lambbins, range=None)[0]
            # lamb = 0.5*(lambbins[1:] + lambbins[:-1])
            # phi = 0.5*(phibins[1:] + phibins[:-1])
        # else:
            # datavert = np.nanmean(data, axis=1)
            # data = np.nanmean(data, axis=2)
            # lamb = lamb[:, 0]
            # phi = phi[0, :]

        # # bsplines modulation of bck and amp, if relevant
        # # fit bsplines on datavert (vertical profile)
        # # to modulate scales (bck and amp)

        # dscales['bs'] = np.full((nspect, dinput['nbs']), np.nan)
        # for ii in dinput['valid']['indt'].nonzero()[0]:
            # indnonan = ~np.isnan(datavert[ii, :])
            # bs = scpinterp.LSQUnivariateSpline(
                # phi[indnonan], datavert[ii, indnonan],
                # dinput['knots'][1:-1],
                # k=dinput['deg'],
                # bbox=dinput['knots'][np.r_[0,-1]],
                # ext=0)
            # dscales['bs'][ii, :] = bs.get_coeffs()
        # # Normalize to avoid double-amplification when amp*bs
        # corr = np.max(dscales['bs'][dinput['valid']['indt'], :],
                      # axis=1)[:, None]
        # dscales['bs'][dinput['valid']['indt'], :] /= corr

    # --------------
    # Default values for filling missing fields
    Dlamb = np.diff(dinput['dprepare']['domain']['lamb']['minmax'])
    lambm = dinput['dprepare']['domain']['lamb']['minmax'][0]

    # bck
    dx0 = _fit12d_filldef_dscalesx0_float(
        din=dx0, din_name='dx0', key='bck', vref=1., nspect=nspect,
    )

    # amp
    dx0 = _fit12d_filldef_dscalesx0_dict(
        din=dx0, din_name='dx0', key='amp', vref=1.,
        nspect=nspect, dinput=dinput,
    )

    # width
    dx0 = _fit12d_filldef_dscalesx0_dict(
        din=dx0, din_name='dx0', key='width', vref=1.,
        nspect=nspect, dinput=dinput,
    )

    # shift
    dx0 = _fit12d_filldef_dscalesx0_dict(
        din=dx0, din_name='dx0', key='shift', vref=1.,
        nspect=nspect, dinput=dinput,
    )

    # Double
    if dinput['double'] is not False:
        dratio = 1.
        dshift = 0.
        if dinput['double'] is True:
            pass
        else:
            if dinput['double'].get('dratio') is not None:
                dratio = dinput['double']['dratio']
            if dinput['double'].get('dshift') is not None:
                dratio = dinput['double']['dshift']
        dx0 = _fit12d_filldef_dscalesx0_float(
            din=dx0, din_name='dx0', key='dratio', vref=dratio, nspect=nspect,
        )
        dx0 = _fit12d_filldef_dscalesx0_float(
            din=dx0, din_name='dx0', key='dshift', vref=dshift, nspect=nspect,
        )
    return dx0


def _checkformat_dx0(dx0=None, dinput=None):

    # -----------------
    # Check preliminary
    c0 = dx0 is None
    c1 = (
        isinstance(dx0, dict)
        and all([
            k0 in ['bck', 'amp', 'width', 'shift', 'dratio', 'dshift']
            and isinstance(v0, dict)
            and all([
                k1 in dinput[k0].keys() and type(v1) in _LTYPES
                for k1 in v0.keys()
            ])
            for k0, v0 in dx0.items()
        ])
    )

    if not any([c0, c1]):
        msg = ("dx0 must be None or a dict of the form:\n"
               + "\t{'amp': {'a0': float, 'a1': float, ...},\n"
               + "\t 'width': {'w0': float, 'w1': float, ...},\n"
               + "\t 'shift': {'s0': float, 's1': float, ...}\n"
               + "  where, as defined in dconstraints:\n"
               + "\t- [a0, a1, ...] are keys of amp groups\n"
               + "\t- [w0, w1, ...] are keys of width groups\n"
               + "\t- [s0, s1, ...] are keys of shift groups\n\n"
               + "You provided:\n{}".format(dx0))
        raise Exception(msg)

    # -----------------
    # Build
    if c0:
        dx0 = {}

    dx0['bck'] = dx0.get('bck', 1.)
    for kk, vv in [('amp', 1.), ('width', 1.), ('shift', 0.)]:
        dx0[kk] = {
            k1: dx0.get(kk, {kk: {k1: vv}}).get(k1, vv)
            for k1 in dinput[kk].keys()
        }

    # double
    if dinput['double'] is not False:
        dx0['dratio'] = dx0.get('dratio', 1.)
        dx0['dshift'] = dx0.get('dshift', 0.)
    return dx0


# DEPRECATED ?
def multigausfit12d_from_dlines_x0(dind=None, nbs=None,
                                   double=None, dx0=None,
                                   nspect=None, keys=None):

    # Only difference between 1d and 2d
    iax = dind['amp']['x']
    if nbs is not None:
        dx0['amp'] = np.repeat(dx0['amp'], nbs)
        iax = iax.T.ravel()

    # Each x0 should be understood as x0*scale
    x0_scale = np.full((nspect, dind['sizex']), np.nan)
    x0_scale[:, iax] = dx0['amp'] # / scales[?]
    x0_scale[:, dind['bck']['x']] = 1.
    x0_scale[:, dind['width']['x']] = dx0['width']
    x0_scale[:, dind['shift']['x']] = dx0['shift']
    if double is not False:
        if double is True:
            x0_scale[:, dind['dratio']['x']] = 0.7
            x0_scale[:, dind['dshift']['x']] = 0.7
        else:
            if double.get('dratio') is None:
                x0_scale[:, dind['dratio']['x']] = 0.7
            if double.get('dshift') is None:
                x0_scale[:, dind['dshift']['x']] = 0.7
    return x0_scale


# TBC / TBF
def fit12d_dx0(dx0=None, dinput=None):

    dx0 = _checkformat_dx0(dx0=dx0, dinput=dinput)

    # Only difference between 1d and 2d
    iax = dind['amp']['x']
    if nbs is not None:
        dx0['amp'] = np.repeat(dx0['amp'], nbs)
        iax = iax.T.ravel()

    # Each x0 should be understood as x0*scale
    x0_scale = np.full((nspect, dind['sizex']), np.nan)
    x0_scale[:, iax] = dx0['amp'] # / scales[?]
    x0_scale[:, dind['bck']['x']] = 1.
    x0_scale[:, dind['width']['x']] = dx0['width']
    x0_scale[:, dind['shift']['x']] = dx0['shift']
    if double is not False:
        if double is True:
            x0_scale[:, dind['dratio']['x']] = 0.7
            x0_scale[:, dind['dshift']['x']] = 0.7
        else:
            if double.get('dratio') is None:
                x0_scale[:, dind['dratio']['x']] = 0.7
            if double.get('dshift') is None:
                x0_scale[:, dind['dshift']['x']] = 0.7

    # Include at least like dscales: bck amp, shift, width, dratio, dshift


    return dx0



###########################################################
###########################################################
#
#           bounds
#
###########################################################
###########################################################


def multigausfit12d_from_dlines_bounds(sizex=None, dind=None, double=None):
    # Each x0 should be understood as x0*scale
    xup = np.full((sizex,), np.nan)
    xlo = np.full((sizex,), np.nan)
    xup[dind['bck']['x']] = 10.
    xlo[dind['bck']['x']] = 0.
    xup[dind['amp']['x']] = 2
    xlo[dind['amp']['x']] = 0.
    xup[dind['width']['x']] = 2.
    xlo[dind['width']['x']] = 0.01
    xup[dind['shift']['x']] = 2.
    xlo[dind['shift']['x']] = -2.
    if double is not False:
        if double is True:
            xup[dind['dratio']['x']] = 1.6
            xlo[dind['dratio']['x']] = 0.4
            xup[dind['dshift']['x']] = 10.
            xlo[dind['dshift']['x']] = -10.
        else:
            if double.get('dratio') is None:
                xup[dind['dratio']['x']] = 1.6
                xlo[dind['dratio']['x']] = 0.4
            if double.get('dshift') is None:
                xup[dind['dshift']['x']] = 10.
                xlo[dind['dshift']['x']] = -10.
    bounds_scale = (xlo, xup)
    return bounds_scale


###########################################################
###########################################################
#
#           Load dinput
#
###########################################################
###########################################################


def _rebuild_dict(dd):
    for k0, v0 in dd.items():
        if isinstance(v0, np.ndarray) and v0.shape == ():
            dd[k0] = v0.tolist()
        if isinstance(dd[k0], dict):
            _rebuild_dict(dd[k0])


def _checkformat_dinput(dinput):
    if isinstance(dinput, str):
        if not os.path.isfile(dinput) or dinput[-4:] != '.npz':
            msg = ("Arg dinput must be aither a dict or "
                   + "the absolute path to a .npz\n"
                   + "  You provided: {}".format(dinput))
            raise Exception(msg)
        dinput = dict(np.load(dinput, allow_pickle=True))

    if not isinstance(dinput, dict):
        msg = ("dinput must be a dict!\n"
               + "  You provided: {}".format(type(dinput)))

    _rebuild_dict(dinput)
    return dinput


###########################################################
###########################################################
#
#           Main fitting sub-routines
#
###########################################################
###########################################################


def _checkformat_options(chain, method, tr_solver, tr_options,
                         xtol, ftol, gtol, loss, max_nfev, verbose):
    if chain is None:
        chain = _CHAIN
    if method is None:
        method = _METHOD
    assert method in ['trf', 'dogbox'], method
    if tr_solver is None:
        tr_solver = None
    if tr_options is None:
        tr_options = {}
    if xtol is None:
        xtol = _TOL1D['x']
    if ftol is None:
        ftol = _TOL1D['f']
    if gtol is None:
        gtol = _TOL1D['g']
    if loss is None:
        loss = _LOSS
    if max_nfev is None:
        max_nfev = None
    if verbose is None:
        verbose = 1
    if verbose == 3:
        verbscp = 2
    else:
        verbscp = 0

    return (chain, method, tr_solver, tr_options,
            xtol, ftol, gtol, loss, max_nfev, verbose, verbscp)


def multigausfit1d_from_dlines(dinput=None, dx0=None,
                               scales=None, dscales=None, bounds_scale=None,
                               method=None, tr_solver=None, tr_options=None,
                               xtol=None, ftol=None, gtol=None,
                               max_nfev=None, chain=None, verbose=None,
                               loss=None, jac=None):
    """ Solve multi_gaussian fit in 1d from dlines

    If double is True, all lines are double with common shift and ratio

    Unknowns are:
        x = [bck, w0, v0, c00, c01, ..., c0n, w1, v1, c10, c11, ..., c1N, ...]

        - bck : constant background
        - wi  : spectral width of a group of lines (ion): wi^2 = 2kTi / m*c**2
                This way, it is dimensionless
        - vni : normalised velicity of the ion: vni = vi / c
        - cij : normalised coef (intensity) of line: cij = Aij

    Scaling is done so each quantity is close to unity:
        - bck: np.mean(data[data < mean(data)/2])
        - wi : Dlamb / 20
        - vni: 10 km/s
        - cij: np.mean(data)

    """

    # ---------------------------
    # Check format options
    (chain, method, tr_solver, tr_options,
    xtol, ftol, gtol, loss, max_nfev,
     verbose, verbscp) = _checkformat_options(
         chain, method, tr_solver, tr_options,
         xtol, ftol, gtol, loss, max_nfev, verbose)

    # ---------------------------
    # Load dinput if necessary
    dinput = _checkformat_dinput(dinput)
    dprepare, dind = dinput['dprepare'], dinput['dind']
    nspect = dprepare['data'].shape[0]

    # ---------------------------
    # If same spectrum => consider a single data set
    if dinput['same_spectrum'] is True:
        lamb = (dinput['same_spectrum_dlamb']*np.arange(0, nspect)[:, None]
                + dprepare['lamb'][None, :]).ravel()
        data = dprepare['data'].ravel()[None, :]
        nspect = data.shape[0]
        chain = False
    else:
        lamb = dprepare['lamb']
        data = dprepare['data']

    # ---------------------------
    # Get scaling
    scales = multigausfit1d_from_dlines_scale(
        data, lamb,
        domain=dprepare['domain'], dinput=dinput,
        dind=dind, scales=scales, dscales=dscales, nspect=nspect)

    # ---------------------------
    # Get initial guess
    dx0 = _checkformat_dx0(dx0=dx0, dinput=dinput, scales=scales)

    # with scaling
    x0_scale = multigausfit12d_from_dlines_x0(
        dind=dind, double=dinput['double'], nspect=nspect,
        dx0=dx0, keys=dinput['keys'])

    # ---------------------------
    # get bounds
    bounds_scale = multigausfit12d_from_dlines_bounds(dind['sizex'],
                                                      dind,
                                                      dinput['double'])

    # ---------------------------
    # Get function, cost function and jacobian
    (func_detail, func_cost,
     func_jac) = _funccostjac.multigausfit1d_from_dlines_funccostjac(
         lamb, dinput=dinput, dind=dind, jac=jac)

    # ---------------------------
    # Prepare output
    datacost = dprepare['data']
    sol_x = np.full((nspect, dind['sizex']), np.nan)
    success = np.full((nspect,), np.nan)
    time = np.full((nspect,), np.nan)
    cost = np.full((nspect,), np.nan)
    nfev = np.full((nspect,), np.nan)
    validity = np.zeros((nspect,), dtype=int)
    message = ['' for ss in range(nspect)]
    errmsg = ['' for ss in range(nspect)]

    # Prepare msg
    if verbose in [1, 2]:
        col = np.char.array(['Spect', 'time (s)', 'cost',
                             'nfev', 'njev', 'msg'])
        maxl = max(np.max(np.char.str_len(col)), 10)
        msg = '\n'.join([' '.join([cc.ljust(maxl) for cc in col]),
                         ' '.join(['-'*maxl]*6)])
        print(msg)

    # ---------------------------
    # Main loop
    end = '\r'
    t0 = dtm.datetime.now()     # DB
    for ii in range(nspect):

        if verbose == 3:
            msg = "\nSpect {} / {}".format(ii+1, nspect)
            print(msg)

        try:
            dti = None
            t0i = dtm.datetime.now()     # DB
            if not dinput['valid']['indt'][ii]:
                continue

            # optimization
            res = scpopt.least_squares(
                func_cost, x0_scale[ii, :],
                jac=func_jac, bounds=bounds_scale,
                method=method, ftol=ftol, xtol=xtol,
                gtol=gtol, x_scale=1.0, f_scale=1.0,
                loss=loss, diff_step=None,
                tr_solver=tr_solver, tr_options=tr_options,
                jac_sparsity=None, max_nfev=max_nfev,
                verbose=verbscp, args=(),
                kwargs={'data': datacost[ii, :],
                        'scales': scales[ii, :],
                        'indok': dprepare['indok'][ii, :]})
            dti = (dtm.datetime.now() - t0i).total_seconds()

            if chain is True and ii < nspect-1:
                x0_scale[ii+1, :] = res.x

            # cost, message, time
            success[ii] = res.success
            cost[ii] = res.cost
            nfev[ii] = res.nfev
            message[ii] = res.message
            time[ii] = round((dtm.datetime.now()-t0i).total_seconds(),
                             ndigits=3)
            sol_x[ii, :] = res.x

        except Exception as err:
            errmsg[ii] = str(err)
            validity[ii] = -1

        # Verbose
        if verbose in [1, 2]:
            if validity[ii] == 0:
                col = np.char.array(['{} / {}'.format(ii+1, nspect),
                                     '{}'.format(dti),
                                     '{:5.3e}'.format(res.cost),
                                     str(res.nfev), str(res.njev),
                                     res.message])
            else:
                col = np.char.array(['{} / {}'.format(ii+1, nspect),
                                     '{}'.format(dti),
                                     ' - ', ' - ', ' - ',
                                     errmsg[ii]])
            msg = ' '.join([cc.ljust(maxl) for cc in col])
            if verbose == 1:
                if ii == nspect-1:
                    end = '\n'
                print(msg, end=end, flush=True)
            else:
                print(msg, end='\n')

    # ---------------------------
    # Reshape in case of same_spectrum
    if dinput['same_spectrum'] is True:
        nspect0 = dinput['same_spectrum_nspect']
        def reshape_custom(aa, nspect0=nspect0):
            return aa.reshape((nspect0, int(aa.size/nspect0)))
        nlamb = int(lamb.size / nspect0)
        nlines = int((sol_detail.shape[1]-1)/nspect0)
        lamb = lamb[:nlamb]

        nxbis = int(dind['bck']['x'].size
                    + (dind['amp']['x'].size + dind['width']['x'].size)/nspect0
                    + dind['shift']['x'].size)
        if dinput['double'] is not False:
            if dinput['double'] is True:
                nxbis += 2
            else:
                nxbis += (dinput['double'].get('dratio') is not None
                          + dinput['double'].get('dshift') is not None)
        nb = dind['bck']['x'].size
        na = int(dind['amp']['x'].size/nspect0)
        nw = int(dind['width']['x'].size/nspect0)
        ns = dind['shift']['x'].size
        x2 = np.full((nspect0, nxbis), np.nan)
        x2[:, :nb] = sol_x[0, dind['bck']['x']][None, :]
        x2[:, nb:nb+na] = reshape_custom(sol_x[0, dind['amp']['x']])
        x2[:, nb+na:nb+na+nw] = reshape_custom(sol_x[0, dind['width']['x']])
        x2[:, nb+na+nw:nb+na+nw+ns] = sol_x[:, dind['shift']['x']]
        if dinput['double'] is True:
            x2[:, dind['dratio']['x']] = sol_x[:, dind['dratio']['x']]
            x2[:, dind['dshift']['x']] = sol_x[:, dind['dshift']['x']]
        import pdb; pdb.set_trace()     # DB
        sol_x = x2

    # Isolate dratio and dshift
    dratio, dshift = None, None
    if dinput['double'] is not False:
        if dinput['double'] is True:
            dratio = (sol_x[:, dind['dratio']['x']]
                      * scales[:, dind['dratio']['x']])
            dshift = (sol_x[:, dind['dshift']['x']]
                      * scales[:, dind['dshift']['x']])
        else:
            if dinput['double'].get('dratio') is None:
                dratio = (sol_x[:, dind['dratio']['x']]
                          * scales[:, dind['dratio']['x']])
            else:
                dratio = np.full((nspect,), dinput['double']['dratio'])
            if dinput['double'].get('dshift') is None:
                dshift = (sol_x[:, dind['dshift']['x']]
                          * scales[:, dind['dshift']['x']])
            else:
                dshift = np.full((nspect,), dinput['double']['dshift'])

    if verbose > 0:
        dt = (dtm.datetime.now()-t0).total_seconds()
        msg = ("Total computation time:"
               + "\t{} s for {} spectra ({} s per spectrum)".format(
                   round(dt, ndigits=3), nspect,
                   round(dt/nspect, ndigits=3)))
        print(msg)

    # ---------------------------
    # Format output as dict
    dfit = {'dinput': dinput,
            'scales': scales, 'x0_scale': x0_scale,
            'bounds_scale': bounds_scale,
            'jac': jac, 'sol_x': sol_x,
            'dratio': dratio, 'dshift': dshift,
            'time': time, 'success': success,
            'validity': validity, 'errmsg': np.array(errmsg),
            'cost': cost, 'nfev': nfev, 'msg': np.array(message)}
    return dfit


def multigausfit2d_from_dlines(dinput=None, dx0=None,
                               scales=None, dscales=None,
                               x0_scale=None, bounds_scale=None,
                               method=None, tr_solver=None, tr_options=None,
                               xtol=None, ftol=None, gtol=None,
                               max_nfev=None, chain=None, verbose=None,
                               loss=None, jac=None):
    """ Solve multi_gaussian fit in 1d from dlines

    If double is True, all lines are double with common shift and ratio

    Unknowns are:
        x = [bck, w0, v0, c00, c01, ..., c0n, w1, v1, c10, c11, ..., c1N, ...]

        - bck : constant background
        - wi  : spectral width of a group of lines (ion): wi^2 = 2kTi / m*c**2
                This way, it is dimensionless
        - vni : normalised velicity of the ion: vni = vi / c
        - cij : normalised coef (intensity) of line: cij = Aij

    Scaling is done so each quantity is close to unity:
        - bck: np.mean(data[data < mean(data)/2])
        - wi : Dlamb / 20
        - vni: 10 km/s
        - cij: np.mean(data)

    """

    # ---------------------------
    # Check format options
    (chain, method, tr_solver, tr_options,
     xtol, ftol, gtol, loss, max_nfev,
     verbose, verbscp) = _checkformat_options(
         chain, method, tr_solver, tr_options,
         xtol, ftol, gtol, loss, max_nfev, verbose)

    # ---------------------------
    # Load dinput if necessary
    dinput = _checkformat_dinput(dinput)
    dprepare, dind = dinput['dprepare'], dinput['dind']
    nspect = dprepare['data'].shape[0]

    # ---------------------------
    # Get scaling
    phi2 = dprepare['phi']
    if dinput['symmetry'] is True:
        phi2 = np.abs(phi2 - np.nanmean(dinput['symmetry_axis']))

    scales = multigausfit12d_from_dlines_scale(
        dprepare['data'], dprepare['lamb'], phi2,
        domain=dprepare['domain'], dinput=dinput,
        dind=dind, scales=scales, dscales=dscales, nspect=nspect)

    # ---------------------------
    # Get initial guess
    x0_scale = multigausfit2d_from_dlines_x0(
        dind=dind, double=dinput['double'],
        dx0=dx0, keys=dinput['keys'],
        nspect=nspect, nbs=dinput['nbs'])

    # ---------------------------
    # get bounds
    bounds_scale = multigausfit2d_from_dlines_bounds(dind['sizex'],
                                                     dind,
                                                     dinput['double'])

    # ---------------------------
    # Get function, cost function and jacobian
    (func_detail, func_cost,
     func_jac) = _funccostjac.multigausfit2d_from_dlines_funccostjac(
         dprepare['lamb'], phi2, indok=dprepare['indok'],
         binning=dprepare['binning'], dinput=dinput,
         dind=dind, jac=jac)

    # ---------------------------
    # Prepare output
    datacost = np.reshape(
        dprepare['data'][:, dprepare['indok']],
        (nspect, dprepare['indok'].sum()))
    sol_x = np.full((nspect, dind['sizex']), np.nan)
    success = np.full((nspect,), np.nan)
    time = np.full((nspect,), np.nan)
    cost = np.full((nspect,), np.nan)
    nfev = np.full((nspect,), np.nan)
    validity = np.zeros((nspect,), dtype=int)
    message = ['' for ss in range(nspect)]
    errmsg = ['' for ss in range(nspect)]

    if dprepare.get('indok_var') is not None:
        msg = ('indok_var not implemented yet!')
        raise Exception(msg)
        if dprepare['indok_var'].ndim == 3:
            indok_var = dprepare['indok_var'].reshape(
                (nspect, dprepare['lamb'].size))
        else:
            indok_var = [dprepare['indok_var'].ravel()]*nspect
    else:
        indok_var = [False]*nspect
    dprepare['indok_var'] = indok_var

    # Prepare msg
    if verbose in [1, 2]:
        col = np.char.array(['Spect', 'time (s)', 'cost',
                             'nfev', 'njev', 'msg'])
        maxl = max(np.max(np.char.str_len(col)), 10)
        msg = '\n'.join([' '.join([cc.ljust(maxl) for cc in col]),
                         ' '.join(['-'*maxl]*6)])
        print(msg)

    # ---------------------------
    # Minimize
    end = '\r'
    t0 = dtm.datetime.now()     # DB
    for ii in range(nspect):
        if verbose == 3:
            msg = "\nSpect {} / {}".format(ii+1, nspect)
            print(msg)
        try:
            t0i = dtm.datetime.now()     # DB
            if not dinput['valid']['indt'][ii]:
                continue
            res = scpopt.least_squares(
                func_cost, x0_scale[ii, :],
                jac=func_jac, bounds=bounds_scale,
                method=method, ftol=ftol, xtol=xtol,
                gtol=gtol, x_scale=1.0, f_scale=1.0,
                loss=loss, diff_step=None,
                tr_solver=tr_solver, tr_options=tr_options,
                jac_sparsity=None, max_nfev=max_nfev,
                verbose=verbscp, args=(),
                kwargs={'data': datacost[ii, :],
                        'scales': scales[ii, :],
                        'indok_var': indok_var[ii],
                        'ind_bs': dinput['valid']['indbs'][ii, :]})
            dti = (dtm.datetime.now() - t0i).total_seconds()

            if chain is True and ii < nspect-1:
                x0_scale[ii+1, :] = res.x

            # cost, message, time
            success[ii] = res.success
            cost[ii] = res.cost
            nfev[ii] = res.nfev
            message[ii] = res.message
            time[ii] = round((dtm.datetime.now()-t0i).total_seconds(),
                             ndigits=3)
            sol_x[ii, :] = res.x

        except Exception as err:
            errmsg[ii] = str(err)
            validity[ii] = -1

        if verbose in [1, 2]:
            if validity[ii] == 0:
                col = np.char.array(['{} / {}'.format(ii+1, nspect),
                                     '{}'.format(dti),
                                     '{:5.3e}'.format(res.cost),
                                     str(res.nfev), str(res.njev),
                                     res.message])
            else:
                col = np.char.array(['{} / {}'.format(ii+1, nspect),
                                     '{}'.format(dti),
                                     ' - ', ' - ', ' - ',
                                     errmsg[ii]])
            msg = ' '.join([cc.ljust(maxl) for cc in col])
            if verbose == 1:
                if ii == nspect-1:
                    end = '\n'
                print(msg, end=end, flush=True)
            else:
                print(msg, end='\n')

    # Isolate dratio and dshift
    dratio, dshift = None, None
    if dinput['double'] is not False:
        if dinput['double'] is True:
            dratio = (sol_x[:, dind['dratio']['x']]
                      * scales[:, dind['dratio']['x']])
            dshift = (sol_x[:, dind['dshift']['x']]
                      * scales[:, dind['dshift']['x']])
        else:
            if dinput['double'].get('dratio') is None:
                dratio = (sol_x[:, dind['dratio']['x']]
                          * scales[:, dind['dratio']['x']])
            else:
                dratio = np.full((nspect,), dinput['double']['dratio'])
            if dinput['double'].get('dshift') is None:
                dshift = (sol_x[:, dind['dshift']['x']]
                          * scales[:, dind['dshift']['x']])
            else:
                dshift = np.full((nspect,), dinput['double']['dshift'])

    if verbose > 0:
        dt = (dtm.datetime.now()-t0).total_seconds()
        msg = ("Total computation time:"
               + "\t{} s for {} spectra ({} s per spectrum)".format(
                   round(dt, ndigits=3), nspect,
                   round(dt/nspect, ndigits=3)))
        print(msg)

    # ---------------------------
    # Format output as dict
    dfit = {'dinput': dinput,
            'scales': scales, 'x0_scale': x0_scale,
            'bounds_scale': bounds_scale, 'phi2': phi2,
            'jac': jac, 'sol_x': sol_x,
            'dratio': dratio, 'dshift': dshift,
            'time': time, 'success': success,
            'validity': validity, 'errmsg': np.array(errmsg),
            'cost': cost, 'nfev': nfev, 'msg': np.array(message)}
    return dfit


###########################################################
###########################################################
#
#   Main fit functions
#
###########################################################
###########################################################


def fit1d(
    dinput=None,
    method=None, tr_solver=None, tr_options=None,
    xtol=None, ftol=None, gtol=None,
    max_nfev=None, loss=None, chain=None,
    dx0=None, x0_scale=None, bounds_scale=None,
    jac=None, verbose=None, showonly=None,
    save=None, name=None, path=None,
    amp=None, coefs=None, ratio=None,
    Ti=None, width=None,
    vi=None, shift=None,
    pts_lamb_total=None, pts_lamb_detail=None,
    plot=None, fs=None, wintit=None, tit=None, dmargin=None,
    return_dax=None):

    # ----------------------
    # Check / format
    if showonly is None:
        showonly = False
    if save is None:
        save = False
    if plot is None:
        plot = False
    if return_dax is None:
        return_dax = False

    # ----------------------
    # Get dinput for 1d fitting from dlines, dconstraints, dprepare...
    if not isinstance(dinput, dict):
        msg = ("Please provide a properly formatted dict of inputs!\n"
               + "fit1d() needs the problem to be given as a dinput dict\n"
               + "  => Use dinput = fit1d_dinput()")
        raise Exception(msg)

    # ----------------------
    # Perform 2d fitting
    if showonly is True:
        msg = "TBF: lambfit and spect1d not defined"
        raise Exception(msg)

        dfit1d = {'shift': np.zeros((1, dinput['nlines'])),
                  'coefs': np.zeros((1, dinput['nlines'])),
                  'lamb': lambfit,
                  'data': spect1d,
                  'double': False,
                  'Ti': False,
                  'vi': False,
                  'ratio': None}
    else:
        dfit1d = multigausfit1d_from_dlines(
            dinput=dinput,
            dx0=dx0, dscales=dscales, bounds_scale=bounds_scale,
            method=method, max_nfev=max_nfev,
            tr_solver=tr_solver, tr_options=tr_options,
            xtol=xtol, ftol=ftol, gtol=gtol, loss=loss,
            chain=chain, verbose=verbose, jac=jac)

    # ----------------------
    # Optional saving
    if save is True:
        if name is None:
            name = 'custom'
        name = 'TFS_fit1d_doutput_{}_nbs{}_{}_tol{}_{}.npz'.format(
            name, dinput['nbs'], dinput['method'], dinput['xtol'])
        if name[-4:] != '.npz':
            name = name + '.npz'
        if path is None:
            path = './'
        pfe = os.path.join(os.path.abspath(path), name)
        np.savez(pfe, **dfit2d)
        msg = ("Saved in:\n"
               + "\t{}".format(pfe))
        print(msg)

    # ----------------------
    # Optional plotting
    if plot is True:
        dout = fit1d_extract(
            dfit1d,
            amp=amp, coefs=coefs, ratio=ratio,
            Ti=Ti, width=width, vi=vi, shift=shift,
            pts_lamb_total=pts_lamb_total,
            pts_lamb_detail=pts_lamb_detail)
        # TBF
        dax = _plot.plot_fit1d(
            dfit1d=dfit1d, dout=dout, showonly=showonly,
            fs=fs, dmargin=dmargin,
            tit=tit, wintit=wintit)

    # ----------------------
    # return
    if return_dax is True:
        return dfit1d, dax
    else:
        return dfit1d

# TBF
def fit2d(dinput=None, dprepare=None, dlines=None, dconstraints=None,
          lamb=None, phi=None, data=None, mask=None,
          domain=None, pos=None, subset=None, binning=None,
          deg=None, knots=None, nbsplines=None,
          method=None, tr_solver=None, tr_options=None,
          xtol=None, ftol=None, gtol=None,
          max_nfev=None, loss=None, chain=None,
          dx0=None, x0_scale=None, bounds_scale=None,
          jac=None, nxi=None, nxj=None, verbose=None, showonly=None,
          save=None, name=None, path=None,
          amp=None, coefs=None, ratio=None,
          Ti=None, width=None,
          vi=None, shift=None,
          pts_lamb_total=None, pts_lamb_detail=None,
          plot=None, fs=None, wintit=None, tit=None, dmargin=None,
          return_dax=None):

    # ----------------------
    # Check / format
    if showonly is None:
        showonly = False
    if save is None:
        save = False
    if plot is None:
        plot = False
    if return_dax is None:
        return_dax = False

    # ----------------------
    # Get dinput for 2d fitting from dlines, dconstraints, dprepare...
    if dinput is None:
        dinput = fit2d_dinput(
            dlines=dlines, dconstraints=dconstraints, dprepare=dprepare,
            data=data, lamb=lamb, phi=phi,
            mask=mask, domain=domain,
            pos=pos, subset=subset, binning=binning,
            nxi=nxi, nxj=nxj, lphi=None, lphi_tol=None,
            deg=deg, knots=knots, nbsplines=nbsplines)

    # ----------------------
    # Perform 2d fitting
    if showonly is True:
        # TBF
        pass
    else:
        dfit2d = multigausfit2d_from_dlines(
            dinput=dinput, dx0=dx0,
            x0_scale=x0_scale, bounds_scale=bounds_scale,
            method=method, max_nfev=max_nfev,
            tr_solver=tr_solver, tr_options=tr_options,
            xtol=xtol, ftol=ftol, gtol=gtol, loss=loss,
            chain=chain, verbose=verbose, jac=jac)

    # ----------------------
    # Optional saving
    if save is True:
        if name is None:
            name = 'custom'
        name = 'TFS_fit2d_doutput_{}_nbs{}_{}_tol{}_{}.npz'.format(
            name, dinput['nbs'], dinput['method'], dinput['xtol'])
        if name[-4:] != '.npz':
            name = name + '.npz'
        if path is None:
            path = './'
        pfe = os.path.join(os.path.abspath(path), name)
        np.savez(pfe, **dfit2d)
        msg = ("Saved in:\n"
               + "\t{}".format(pfe))
        print(msg)

    # ----------------------
    # Optional plotting
    if plot is True:
        dout = fit2d_extract(dfit2d)
        dax = None

    # ----------------------
    # return
    if return_dax is True:
        return dfit2d, dax
    else:
        return dfit2d


###########################################################
###########################################################
#
#   Extract data from pre-computed dict of fitted results
#
###########################################################
###########################################################


def fit12d_get_data_checkformat(dfit=None,
                                pts_phi=None, npts_phi=None,
                                amp=None, coefs=None, ratio=None,
                                Ti=None, width=None,
                                vi=None, shift=None,
                                pts_total=None, pts_detail=None,
                                allow_pickle=None):

    # load file if str
    if isinstance(dfit, str):
        if not os.path.isfile(dfit) or not dfit[-4:] == '.npz':
            msg = ("Provided dfit must be either a dict or "
                   + "the absolute path to a saved .npz\n"
                   + "  You provided: {}".format(dfit))
            raise Exception(msg)
        if allow_pickle is None:
            allow_pickle = _ALLOW_PICKLE
        dfit = dict(np.load(dfit, allow_pickle=allow_pickle))
        _rebuild_dict(dfit)

    # check dfit basic structure
    lk = ['dprepare', 'dinput', 'dind', 'sol_x', 'jac', 'scales']
    c0 = (isinstance(dfit, dict)
          and all([ss in dfit.keys() for ss in lk]))
    if not isinstance(dfit, dict):
        msg = ("dfit must be a dict with at least the following keys:\n"
               + "\t- {}\n".format(lk)
               + "\t- provided: {}".format(dfit))
        raise Exception(msg)

    # Identify if fit1d or fit2d
    is2d = 'nbsplines' in dfit['dinput'].keys()
    if is2d is True and not 'phi2' in dfit.keys():
        msg = "dfit is a fit2d output but does not have key 'phi2'!"
        raise Exception(msg)

    # Extract dinput and dprepare (more readable)
    dinput = dfit['dinput']
    dprepare = dfit['dinput']['dprepare']

    # ratio
    if ratio is None:
        ratio = False
    if ratio is not False:
        coefs = True

    # Check / format amp, Ti, vi
    d3 = {'amp': [amp, 'amp'],
          'coefs': [coefs, 'amp'],
          'Ti': [Ti, 'width'],
          'width': [width, 'width'],
          'vi': [vi, 'shift'],
          'shift': [shift, 'shift']}
    # amp, Ti, vi
    for k0 in d3.keys():
        if d3[k0][0] is None:
            d3[k0][0] = True
        if d3[k0][0] is True:
            d3[k0][0] = _D3[k0]
        if d3[k0][0] is False:
            continue
        lc = [d3[k0][0] in ['lines', 'x'],
              isinstance(d3[k0][0], str),
              (isinstance(d3[k0][0], list)
               and all([isinstance(isinstance(ss, str) for ss in d3[k0][0])]))]
        if not any(lc):
            msg = ("Arg {} must be either:\n".format(k0)
                   + "\t- 'x': return all unique {}\n".format(k0)
                   + "\t- 'lines': return {} for all lines (inc. duplicates)\n"
                   + "\t- str: a key in:\n"
                   + "\t\t{}\n".format(dinput['keys'])
                   + "\t\t{}\n".format(dinput[d3[k0][1]]['keys'])
                   + "\t- list: a list of keys (see above)\n"
                   + "Provided: {}".format(d3[k0][0]))
            raise Exception(msg)
        if lc[0]:
            if d3[k0][0] == 'lines':
                d3[k0][0] = {'type': d3[k0][0],
                             'ind': np.arange(0, dinput['nlines'])}
            else:
                d3[k0][0] = {
                    'type': d3[k0][0],
                    'ind': np.arange(0, dinput[d3[k0][1]]['keys'].size)}
        elif lc[1]:
            d3[k0][0] = [d3[k0][0]]

        if isinstance(d3[k0][0], list):
            lc = [all([ss in dinput['keys']
                       for ss in d3[k0][0]]),
                  all([ss in dinput[d3[k0][1]]['keys']
                       for ss in d3[k0][0]])]
            if not any(lc):
                msg = ("Arg must contain either keys from:\n"
                       + "\t- lines keys: {}\n".format(dinput['keys'])
                       + "\t- {} keys: {}".format(k0,
                                                  dinput[d3[k0][1]]['keys']))
                raise Exception(msg)
            if lc[0]:
                d3[k0][0] = {'type': 'lines',
                             'ind': np.array([
                                 (dinput['keys']==ss).nonzero()[0][0]
                                 for ss in d3[k0][0]], dtype=int)}
            else:
                d3[k0][0] = {'type': 'x',
                             'ind': np.array([
                                 (dinput[d3[k0][1]]['keys']==ss).nonzero()[0][0]
                                 for ss in d3[k0][0]], dtype=int)}
        d3[k0][0]['field'] = d3[k0][1]
        d3[k0] = d3[k0][0]


    # Ratio
    if ratio is not False:
        lkeys = dfit['dinput']['keys']
        lc = [isinstance(ratio, tuple),
              isinstance(ratio, list),
              isinstance(ratio, np.ndarray)]
        msg = ("Arg ratio (spectral lines magnitude ratio) must be either:\n"
               + "\t- False:  no line ration computed\n"
               + "\t- tuple of len=2: upper and lower keys of the lines\n"
               + "\t- list of tuple of len=2: upper and lower keys pairs\n"
               + "\t- np.ndarray of shape (2, N): upper keys and lower keys\n"
               + "  You provided: {}\n".format(ratio)
               + "  Available keys: {}".format(lkeys)
              )
        if not any(lc):
            raise Exception(msg)
        if lc[0]:
            c0 = (len(ratio) == 2
                  and all([ss in lkeys for ss in ratio]))
            if not c0:
                raise Exception(msg)
            ratio = np.reshape(ratio, (2, 1))
        elif lc[1]:
            c0 = all([(isinstance(t, tuple)
                       and len(tt) == 2
                       and all([ss in lkeys for ss in tt]))
                      for tt in ratio])
            if not c0:
                raise Exception(msg)
            ratio = np.array(ratio).T
        c0 = (isinstance(ratio, np.ndarray)
              and ratio.ndim == 2
              and ratio.shape[0] == 2
              and all([ss in lkeys for ss in ratio[0, :]])
              and all([ss in lkeys for ss in ratio[1, :]]))
        if not c0:
            raise Exception(msg)

    d3['ratio'] = ratio

    # pts_phi, npts_phi
    if is2d is True:
        c0 = any([v0 is not False for v0 in d3.values()])
        c1 = [pts_phi is not None, npts_phi is not None]
        if all(c1):
            msg = "Arg pts_phi and npts_phi cannot be both provided!"
            raise Exception(msg)
        if not any(c1):
            npts_phi = (2*dinput['deg']-1)*(dinput['knots'].size-1) + 1
        if npts_phi is not None:
            npts_phi = int(npts_phi)
            pts_phi = np.linspace(dprepare['domain']['phi']['minmax'][0],
                                  dprepare['domain']['phi']['minmax'][1],
                                  npts_phi)
        else:
            pts_phi = np.array(pts_phi).ravel()

    # pts_total, pts_detail
    if pts_total is None:
        if dprepare is None:
            pts_total = False
        else:
            if is2d is True:
                pts_total = np.array([dprepare['lamb'], dprepare['phi']])
            else:
                pts_total = dprepare['lamb']
    if pts_detail is None:
        pts_detail = False
    if pts_detail is True and pts_total is not False:
        pts_detail = pts_total
    if pts_detail is not False:
        pts_detail = np.array(pts_detail)
    if pts_total is not False:
        pts_total = np.array(pts_total)

    return d3, pts_phi, pts_total, pts_detail


def fit1d_extract(dfit1d=None,
                  amp=None, coefs=None, ratio=None,
                  Ti=None, width=None,
                  vi=None, shift=None,
                  pts_lamb_total=None, pts_lamb_detail=None):

    # -------------------
    # Check format input
    out = fit12d_get_data_checkformat(
        dfit=dfit1d,
        amp=amp, coefs=coefs, ratio=ratio,
        Ti=Ti, width=width,
        vi=vi, shift=shift,
        pts_total=pts_lamb_total,
        pts_detail=pts_lamb_detail)

    d3, pts_phi, pts_lamb_total, pts_lamb_detail = out

    # Extract dprepare and dind (more readable)
    dprepare = dfit1d['dinput']['dprepare']
    dind = dfit1d['dinput']['dind']
    nspect = dprepare['data'].shape[0]

    # Prepare extract func
    def _get_values(key, pts_phi=None,
                    d3=d3, nspect=nspect, dinput=dfit1d['dinput'],
                    dind=dind, sol_x=dfit1d['sol_x'], scales=dfit1d['scales']):
        if d3[key]['type'] == 'lines':
            keys = dinput['keys'][d3[key]['ind']]
        else:
            keys = dinput[d3[key]['field']]['keys'][d3[key]['ind']]
        indbis = dind[d3[key]['field']][d3[key]['type']][d3[key]['ind']]
        val = sol_x[:, indbis] * scales[:, indbis]
        return keys, val

    # -------------------
    # Prepare output
    lk = ['amp', 'coefs', 'ratio', 'Ti', 'width', 'vi', 'shift',
          'dratio', 'dshift']
    dout = dict.fromkeys(lk, False)

    # amp
    if d3['amp'] is not False:
        keys, val = _get_values('amp')
        dout['amp'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # coefs
    if d3['coefs'] is not False:
        keys, val = _get_values('coefs')
        dout['coefs'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # ratio
    if d3['ratio'] is not False:
        nratio = d3['ratio'].shape[1]
        indup = np.r_[[(dout['coefs']['keys'] == kk).nonzero()[0][0]
                       for kk in d3['ratio'][0, :]]]
        indlo = np.r_[[(dout['coefs']['keys'] == kk).nonzero()[0][0]
                       for kk in d3['ratio'][1, :]]]
        val = (dout['coefs']['values'][:, indup]
               / dout['coefs']['values'][:, indlo])
        lab = np.r_[['{} / {}'.format(dfit1d['dinput']['symb'][indup[ii]],
                                      dfit1d['dinput']['symb'][indlo[ii]])
                     for ii in range(nratio)]]
        dout['ratio'] = {'keys': dout['ratio'], 'values': val,
                         'lab': lab, 'units': 'a.u.'}

    # Ti
    if d3['Ti'] is not False:
        keys, val = _get_values('Ti')
        conv = np.sqrt(scpct.mu_0*scpct.c / (2.*scpct.h*scpct.alpha))
        indTi = np.array([iit[0] for iit in dind['width']['jac']])
        # if d3['Ti']['type'] == 'lines':
            # indTi = np.arange(0, dfit1d['dinput']['nlines'])
        indTi = indTi[d3['Ti']['ind']]
        val = (conv * val
               * dfit1d['dinput']['mz'][indTi][None, :]
               * scpct.c**2)
        dout['Ti'] = {'keys': keys, 'values': val, 'units': 'eV'}

    # width
    if d3['width'] is not False:
        keys, val = _get_values('width')
        dout['width'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # vi
    if d3['vi'] is not False:
        keys, val = _get_values('vi')
        val = val * scpct.c
        dout['vi'] = {'keys': keys, 'values': val, 'units': 'm.s^-1'}

    # shift
    if d3['shift'] is not False:
        keys, val = _get_values('shift')
        val = val * dfit1d['dinput']['lines'][None, :]
        dout['shift'] = {'keys': keys, 'values': val, 'units': 'm'}

    # double
    if dfit1d['dinput']['double'] is not False:
        double = dfit1d['dinput']['double']
        if double is True or double.get('dratio') is None:
            dout['dratio'] = dfit1d['sol_x'][:, dind['dratio']['x']]
        else:
            dout['dratio'] = np.full((nspect,), double['dratio'])
        if double is True or double.get('dratio') is None:
            dout['dshift'] = dfit1d['sol_x'][:, dind['dshift']['x']]
        else:
            dout['dshift'] = np.full((nspect,), double['dshift'])

    # -------------------
    # sol_detail and sol_tot
    sold, solt = False, False
    if pts_lamb_detail is not False or pts_lamb_total is not False:

        (func_detail,
         func_cost, _) = _funccostjac.multigausfit1d_from_dlines_funccostjac(
            dprepare['lamb'],
            dinput=dfit1d['dinput'],
            dind=dind, jac=dfit1d['jac'])

        if pts_lamb_detail is not False:
            shape = tuple(np.r_[nspect, pts_lamb_detail.shape,
                                dfit1d['dinput']['nlines']+1])
            sold = np.full(shape, np.nan)
            for ii in range(nspect):
                sold[ii, dprepare['indok'][ii, :], :] = func_detail(
                    dfit1d['sol_x'][ii, :],
                    scales=dfit1d['scales'][ii, :],
                    indok=dprepare['indok'][ii, :])
                    #indok_var=dprepare['indok_var'][ii])

        if pts_lamb_total is not False:
            shape = tuple(np.r_[nspect, pts_lamb_total.shape])
            solt = np.full(shape, np.nan)
            for ii in range(nspect):
                solt[ii, dprepare['indok'][ii, :]] = func_cost(
                    dfit1d['sol_x'][ii, :],
                    scales=dfit1d['scales'][ii, :],
                    indok=dprepare['indok'][ii, :],
                    data=0.)

            # Double-check consistency if possible
            c0 = (pts_lamb_detail is not False
                  and np.allclose(pts_lamb_total, pts_lamb_detail))
            if c0:
                if not np.allclose(solt, np.sum(sold, axis=-1),
                                   equal_nan=True):
                    msg = "Inconsistent computations detail vs total"
                    raise Exception(msg)

    dout['sol_detail'] = sold
    dout['sol_tot'] = solt
    dout['units'] = 'a.u.'

    # -------------------
    # Add input args
    dout['d3'] = d3
    dout['pts_lamb_detail'] = pts_lamb_detail
    dout['pts_lamb_total'] = pts_lamb_total
    return dout


def _get_phi_profile(key,
                     nspect=None, dinput=None,
                     dind=None, sol_x=None, scales=None,
                     typ=None, ind=None, pts_phi=None):
    ncoefs = ind.size
    val = np.full((nspect, pts_phi.size, ncoefs), np.nan)
    BS = BSpline(dinput['knots_mult'],
                 np.ones((dinput['nbs'], ncoefs), dtype=float),
                 dinput['deg'],
                 extrapolate=False, axis=0)
    if typ == 'lines':
        keys = dinput['keys'][ind]
    else:
        keys = dinput[key]['keys'][ind]
    indbis = dind[key][typ][:, ind]
    for ii in range(nspect):
        BS.c = sol_x[ii, indbis] * scales[ii, indbis]
        val[ii, :, :] = BS(pts_phi)
    return keys, val


def fit2d_extract(dfit2d=None,
                  amp=None, coefs=None, ratio=None,
                  Ti=None, width=None,
                  vi=None, shift=None,
                  pts_lamb_phi_total=None, pts_lamb_phi_detail=None):

    # -------------------
    # Check format input
    out = fit12d_get_data_checkformat(
        dfit=dfit2d,
        amp=amp, coefs=coefs, ratio=ratio,
        Ti=Ti, width=width,
        vi=vi, shift=shift,
        pts_total=pts_lamb_total,
        pts_detail=pts_lamb_detail)

    d3, pts_phi, pts_lamb_phi_total, pts_lamb_phi_detail = out

    # Extract dprepare and dind (more readable)
    dprepare = dfit1d['dinput']['dprepare']
    dind = dfit1d['dinput']['dind']
    nspect = dprepare['data'].shape[0]

    # Prepare extract func
    # TBF
    def _get_values(key, pts_phi=None,
                    d3=d3, nspect=nspect, dinput=dfit1d['dinput'],
                    dind=dind, sol_x=dfit1d['sol_x'], scales=dfit1d['scales']):
        if d3[key]['type'] == 'lines':
            keys = dinput['keys'][d3[key]['ind']]
        else:
            keys = dinput[d3[key]['field']]['keys'][d3[key]['ind']]
        indbis = dind[d3[key]['field']][d3[key]['type']][d3[key]['ind']]

        # 1d vs 2d
        if pts_phi is None:
            val = sol_x[:, indbis] * scales[:, indbis]
        else:
            BS = BSpline(dinput['knots_mult'],
                         np.ones((dinput['nbs'], ncoefs), dtype=float),
                         dinput['deg'],
                         extrapolate=False, axis=0)
        for ii in range(nspect):
            BS.c = sol_x[ii, indbis] * scales[ii, indbis]
            val[ii, :, :] = BS(pts_phi)

        return keys, val

    # -------------------
    # Prepare output
    lk = ['amp', 'coefs', 'ratio', 'Ti', 'width', 'vi', 'shift',
          'dratio', 'dshift']
    dout = dict.fromkeys(lk, False)

    # amp
    if d3['amp'] is not False:
        keys, val = _get_values('amp')
        dout['amp'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # coefs
    if d3['coefs'] is not False:
        keys, val = _get_values('coefs')
        dout['coefs'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # ratio
    if d3['ratio'] is not False:
        nratio = d3['ratio'].shape[1]
        indup = np.r_[[(dout['coefs']['keys'] == kk).nonzero()[0][0]
                       for kk in d3['ratio'][0, :]]]
        indlo = np.r_[[(dout['coefs']['keys'] == kk).nonzero()[0][0]
                       for kk in d3['ratio'][1, :]]]
        val = (dout['coefs']['values'][:, indup]
               / dout['coefs']['values'][:, indlo])
        lab = np.r_[['{} / {}'.format(dfit1d['dinput']['symb'][indup[ii]],
                                      dfit1d['dinput']['symb'][indlo[ii]])
                     for ii in range(nratio)]]
        dout['ratio'] = {'keys': dout['ratio'], 'values': val,
                         'lab': lab, 'units': 'a.u.'}

    dout = {}
    # amp
    if d3['amp'] is not False:
        keys, val = _get_phi_profile(
            d3['amp']['field'], nspect=nspect,
            dinput=dfit2d['dinput'],
            dind=dfit2d['dind'], sol_x=dfit2d['sol_x'],
            scales=dfit2d['scales'], pts_phi=pts_phi,
            typ=d3['amp']['type'], ind=d3['amp']['ind'])
        dout['amp'] = {'keys': keys, 'values': val, 'units': 'a.u.'}

    # Ti
    if d3['Ti'] is not False:
        keys, val = _get_phi_profile(
            d3['Ti']['field'], nspect=nspect,
            dinput=dfit2d['dinput'],
            dind=dfit2d['dind'], sol_x=dfit2d['sol_x'],
            scales=dfit2d['scales'], pts_phi=pts_phi,
            typ=d3['Ti']['type'], ind=d3['Ti']['ind'])
        conv = np.sqrt(scpct.mu_0*scpct.c / (2.*scpct.h*scpct.alpha))
        if d3['Ti']['type'] == 'lines':
            indTi = np.arange(0, dfit2d['dinput']['nlines'])
        else:
            indTi = np.array([iit[0]
                              for iit in dfit2d['dind']['width']['jac']])
        indTi = indTi[d3['Ti']['ind']]
        val = (conv * val
               * dfit2d['dinput']['mz'][indTi][None, None, :]
               * scpct.c**2)
        dout['Ti'] = {'keys': keys, 'values': val, 'units': 'eV'}

    # vi
    if d3['vi'] is not False:
        keys, val = _get_phi_profile(
            d3['vi']['field'], nspect=nspect,
            dinput=dfit2d['dinput'],
            dind=dfit2d['dind'], sol_x=dfit2d['sol_x'],
            scales=dfit2d['scales'], pts_phi=pts_phi,
            typ=d3['vi']['type'], ind=d3['vi']['ind'])
        val = val * scpct.c
        dout['vi'] = {'keys': keys, 'values': val, 'units': 'm.s^-1'}

    # -------------------
    # sol_detail and sol_tot
    sold, solt = False, False
    if pts_lamb_phi_detail is not False or pts_lamb_phi_total is not False:

        func_detail = _funccostjac.multigausfit2d_from_dlines_funccostjac(
            dfit2d['dprepare']['lamb'], dfit2d['phi2'],
            indok=dfit2d['dprepare']['indok'],
            binning=dfit2d['dprepare']['binning'],
            dinput=dfit2d['dinput'],
            dind=dfit2d['dind'], jac=dfit2d['jac'])[0]

        if pts_lamb_phi_detail is not False:
            shape = tuple(np.r_[nspect, pts_lamb_phi_detail.shape,
                                dfit2d['dinput']['nlines']+1,
                                dfit2d['dinput']['nbs']])
            sold = np.full(shape, np.nan)
        if pts_lamb_phi_total is not False:
            shape = tuple(np.r_[nspect, pts_lamb_phi_total.shape])
            solt = np.full(shape, np.nan)

        for ii in range(nspect):

            # Separate and reshape output
            fd = func_detail(dfit2d['sol_x'][ii, :],
                             scales=dfit2d['scales'][ii, :],
                             indok_var=dfit2d['dprepare']['indok_var'][ii])

            if pts_lamb_phi_detail is not False:
                sold[ii, ...] = fd
            if pts_lamb_phi_total is not False:
                solt[ii, ...] = np.nansum(np.nansum(fd, axis=-1), axis=-1)

    dout['sol_detail'] = sold
    dout['sol_tot'] = solt
    dout['units'] = 'a.u.'

    # -------------------
    # Add input args
    dout['d3'] = d3
    dout['pts_phi'] = pts_phi
    dout['pts_lamb_phi_detail'] = pts_lamb_phi_detail
    dout['pts_lamb_phi_total'] = pts_lamb_phi_total
    return dout


###########################################################
###########################################################
#
#   Plot fitted data from pre-computed dict of fitted results
#
###########################################################
###########################################################

def fit2d_plot(dout=None):

    # ----------------------
    # Optional plotting
    if plot is True:
        if plotmode is None:
            plotmode = 'transform'
        if indspect is None:
            indspect = 0

        if spect1d is not None:
            # Compute lambfit / phifit and spectrum1d
            if nlambfit is None:
                nlambfit = 200
            ((spect1d, fit1d), lambfit,
             phifit, _, phiminmax) = self._calc_spect1d_from_data2d(
                 [dataflat[indspect, :], dfit2d['sol_tot'][indspect, :]],
                 lambflat, phiflat,
                 nlambfit=nlambfit, nphifit=10,
                 spect1d=spect1d, mask=None, vertsum1d=False)
        else:
            fit1d, lambfit, phiminmax = None, None, None

        dax = _plot_optics.CrystalBragg_plot_data_fit2d(
            xi=xi, xj=xj, data=dfit2d['data'],
            lamb=dfit2d['lamb'], phi=dfit2d['phi'], indspect=indspect,
            indok=indok, dfit2d=dfit2d,
            dax=dax, plotmode=plotmode, angunits=angunits,
            cmap=cmap, vmin=vmin, vmax=vmax,
            spect1d=spect1d, fit1d=fit1d,
            lambfit=lambfit, phiminmax=phiminmax,
            dmargin=dmargin, tit=tit, wintit=wintit, fs=fs)
    return dax


###########################################################
###########################################################
#
#           1d vertical fitting for noise analysis
#
###########################################################
###########################################################


def get_noise_costjac(deg=None, nbsplines=None, dbsplines=None, phi=None,
                      phiminmax=None, symmetryaxis=None, sparse=None):

    if sparse is None:
        sparse = False

    if dbsplines is None:
        dbsplines = multigausfit2d_from_dlines_dbsplines(
            knots=None, deg=deg, nbsplines=nbsplines,
            phimin=phiminmax[0], phimax=phiminmax[1],
            symmetryaxis=symmetryaxis)

    def cost(x,
             km=dbsplines['knots_mult'],
             deg=dbsplines['deg'],
             data=0., phi=phi):
        return scpinterp.BSpline(km, x, deg,
                                 extrapolate=False, axis=0)(phi) - data

    jac = np.zeros((phi.size, dbsplines['nbs']), dtype=float)
    km = dbsplines['knots_mult']
    kpb = dbsplines['nknotsperbs']
    lind = [(phi >= km[ii]) & (phi < km[ii+kpb-1])
            for ii in range(dbsplines['nbs'])]
    if sparse is True:
        def jac_func(x, jac=jac, km=km, data=None,
                     phi=phi, kpb=kpb, lind=lind):
            for ii in range(x.size):
                jac[lind[ii], ii] = scpinterp.BSpline.basis_element(
                    km[ii:ii+kpb], extrapolate=False)(phi[lind[ii]])
            return scpsparse.csr_matrix(jac)
    else:
        def jac_func(x, jac=jac, km=km, data=None,
                     phi=phi, kpb=kpb, lind=lind):
            for ii in range(x.size):
                jac[lind[ii], ii] = scpinterp.BSpline.basis_element(
                    km[ii:ii+kpb], extrapolate=False)(phi[lind[ii]])
            return jac
    return cost, jac_func


def _basic_loop(ilambu=None, ilamb=None, phi=None, data=None, mask=None,
                domain=None, nbs=None, dbsplines=None, nspect=None,
                method=None, tr_solver=None, tr_options=None, loss=None,
                xtol=None, ftol=None, gtol=None, max_nfev=None, verbose=None):

    # ---------------
    # Check inputs
    if method is None:
        method = _METHOD
    assert method in ['trf', 'dogbox', 'lm'], method
    if tr_solver is None:
        tr_solver = None
    if tr_options is None:
        tr_options = {}
    if xtol is None:
        xtol = _TOL2D['x']
    if ftol is None:
        ftol = _TOL2D['f']
    if gtol is None:
        gtol = _TOL2D['g']
    if loss is None:
        loss = _LOSS
    if max_nfev is None:
        max_nfev = None

    x0 = 1. - (2.*np.arange(nbs)/nbs - 1.)**2

    # ---------------
    # Prepare outputs
    dataint = np.full((nspect, ilambu.size), np.nan)
    fit = np.full(data.shape, np.nan)
    indsort = np.zeros((2, phi.size), dtype=int)
    indout_noeval = np.zeros(phi.shape, dtype=bool)
    chi2n = np.full((nspect, ilambu.size), np.nan)
    chi2_meandata = np.full((nspect, ilambu.size), np.nan)

    # ---------------
    # Main loop
    i0, indnan = 0, []
    for jj in range(ilambu.size):
        ind = ilamb == ilambu[jj]
        nind = ind.sum()
        isort = i0 + np.arange(0, nind)

        # skips cases with no points
        if not np.any(ind):
            continue

        inds = np.argsort(phi[ind])
        inds_rev = np.argsort(inds)
        indsort[0, isort] = ind.nonzero()[0][inds]
        indsort[1, isort] = ind.nonzero()[1][inds]

        phisort = phi[indsort[0, isort], indsort[1, isort]]
        datasort = data[:, indsort[0, isort], indsort[1, isort]]
        dataint[:, jj] = np.nanmean(datasort, axis=1)

        # skips cases with to few points
        indok = ~np.any(np.isnan(datasort), axis=0)
        if mask is not None:
            indok &= mask[indsort[0, isort], indsort[1, isort]]

        # Check there are enough phi vs bsplines
        indphimin = np.searchsorted(np.linspace(domain['phi']['minmax'][0],
                                                domain['phi']['minmax'][1],
                                                nbs + 1),
                                    phisort[indok])
        if np.unique(indphimin).size < nbs:
            indout_noeval[ind] = True
            continue
        indout_noeval[ind] = ~indok[inds_rev]

        # get bsplines func
        func_cost, func_jac = get_noise_costjac(phi=phisort[indok],
                                                dbsplines=dbsplines,
                                                sparse=False,
                                                symmetryaxis=False)
        for tt in range(nspect):
            if verbose > 0:
                msg = ("\tlambbin {} / {}".format(jj+1, ilambu.size)
                       + "    "
                       + "time step = {} / {}".format(tt+1, nspect))
                print(msg.ljust(50), end='\r', flush=True)

            if dataint[tt, jj] == 0.:
                continue

            datai = datasort[tt, indok] / dataint[tt, jj]
            res = scpopt.least_squares(
                func_cost, x0, jac=func_jac,
                method=method, ftol=ftol, xtol=xtol, gtol=gtol,
                x_scale='jac', f_scale=1.0, loss=loss, diff_step=None,
                tr_solver=tr_solver, tr_options={}, jac_sparsity=None,
                max_nfev=max_nfev, verbose=0, args=(),
                kwargs={'data': datai})

            # Store in original shape
            fit[tt, ind] = (func_cost(res.x, phi=phisort, data=0.)
                             * dataint[tt, jj])[inds_rev]
            chi2_meandata[tt, jj] = np.nanmean(fit[tt, ind])
            chi2n[tt, jj] = np.nanmean(func_cost(x=res.x, data=datai)**2)

        i0 += nind
        indnan.append(i0)
    return (fit, dataint, indsort, np.array(indnan), indout_noeval,
            chi2n, chi2_meandata)


def noise_analysis_2d(
    data, lamb, phi, mask=None, margin=None, valid_fraction=None,
    deg=None, knots=None, nbsplines=None, nxerrbin=None,
    nlamb=None, loss=None, max_nfev=None,
    xtol=None, ftol=None, gtol=None,
    method=None, tr_solver=None, tr_options=None,
    verbose=None, plot=None,
    ms=None, dcolor=None,
    dax=None, fs=None, dmargin=None,
    wintit=None, tit=None, sublab=None,
    save_fig=None, name_fig=None, path_fig=None, fmt=None,
    return_dax=None):

    # -------------
    # Check inputs
    if not isinstance(nbsplines, int):
        msg = "Please provide a (>0) integer value for nbsplines"
        raise Exception(msg)

    if deg is None:
        deg = 2
    if plot is None:
        plot = True
    if verbose is None:
        verbose = 1
    if return_dax is None:
        return_dax = False

    c0 = lamb.shape == phi.shape == data.shape[1:]
    if c0 is not True:
        msg = ("input data, lamb, phi are non-conform!\n"
               + "\t- expected lamb.shape == phi.shape == data.shape[1:]\n"
               + "\t- provided:\n"
               + "\t\tlamb.shape = {}\n".format(lamb.shape)
               + "\t\tphi.shape = {}\n".format(phi.shape)
               + "\t\tdata.shape = {}\n".format(data.shape)
              )
        raise Exception(msg)

    nspect = data.shape[0]
    domain = {'lamb': {'minmax': [np.nanmin(lamb), np.nanmax(lamb)]},
              'phi': {'minmax': [np.nanmin(phi), np.nanmax(phi)]}}

    if nlamb is None:
        if lamb.ndim == 2:
            nlamb = lamb.shape[0]
        else:
            msg = ("Please provide a value for nlamb (nb of bins)!")
            raise Exception(msg)
    nlamb = int(nlamb)

    # -------------
    # lamb binning
    lambedges = np.linspace(domain['lamb']['minmax'][0],
                            domain['lamb']['minmax'][1], nlamb+1)
    ilamb = np.searchsorted(lambedges, lamb)
    ilambu = np.unique(ilamb)

    # -------------
    # bspline dict and plotting utilities
    dbsplines = multigausfit2d_from_dlines_dbsplines(
        knots=None, deg=deg, nbsplines=nbsplines,
        phimin=domain['phi']['minmax'][0],
        phimax=domain['phi']['minmax'][1],
        symmetryaxis=False)

    # plotting utils
    bs_phi = np.linspace(domain['phi']['minmax'][0],
                         domain['phi']['minmax'][1], 101)
    bs_val = np.array([
        scpinterp.BSpline.basis_element(
            dbsplines['knots_mult'][ii:ii+dbsplines['nknotsperbs']],
            extrapolate=False)(bs_phi)
        for ii in range(nbsplines)]).T

    # -------------
    # Perform fits
    (fit, dataint, indsort, indnan, indout_noeval,
     chi2n, chi2_meandata) = _basic_loop(
        ilambu=ilambu, ilamb=ilamb, phi=phi, data=data, mask=mask,
        domain=domain, nbs=nbsplines, dbsplines=dbsplines, nspect=nspect,
        method=method, tr_solver=tr_solver, tr_options=tr_options, loss=loss,
        xtol=xtol, ftol=ftol, gtol=gtol,
        max_nfev=max_nfev, verbose=verbose)

    # -------------
    # Identify outliers with respect to noise model
    (mean, var, xdata, const,
     indout_var, _, margin, valid_fraction) = get_noise_analysis_var_mask(
         fit=fit, data=data, mask=(mask & (~indout_noeval)),
         margin=margin, valid_fraction=valid_fraction)

    # Safety check
    if mask is None:
        indout_mask = np.zeros(lamb.shape, dtype=bool)
    else:
        indout_mask = ~mask
    indout_noeval[~mask] = False
    indout_tot = np.array([~mask,
                           indout_noeval,
                           np.any(indout_var, axis=0)])
    c0 = np.all(np.sum(indout_tot.astype(int), axis=0) <= 1)
    if not c0:
        msg = "Overlapping indout!"
        raise Exception(msg)

    indin = ~np.any(indout_tot, axis=0)

    # -------------
    # output dict
    dnoise = {
        'data': data, 'phi': phi, 'fit': fit,
        'chi2n': chi2n, 'chi2_meandata': chi2_meandata, 'dataint': dataint,
        'domain': domain, 'indin': indin, 'indout_mask': indout_mask,
        'indout_noeval': indout_noeval, 'indout_var': indout_var,
        'mask': mask, 'ind_noeval': None,
        'indsort': indsort, 'indnan': np.array(indnan),
        'nbsplines': nbsplines, 'bs_phi': bs_phi, 'bs_val': bs_val,
        'deg': deg, 'lambedges': lambedges, 'deg': deg,
        'ilamb': ilamb, 'ilambu': ilambu,
        'var_mean': mean, 'var': var, 'var_xdata': xdata,
        'var_const': const, 'var_margin': margin,
        'var_fraction': valid_fraction}

    # Plot
    if plot is True:
        try:
            dax = _plot.plot_noise_analysis(
                dnoise=dnoise,
                ms=ms, dcolor=dcolor,
                dax=dax, fs=fs, dmargin=dmargin,
                wintit=wintit, tit=tit, sublab=sublab,
                save=save_fig, name=name_fig, path=path_fig, fmt=fmt)
        except Exception as err:
            msg = ("Plotting failed: {}".format(str(err)))
            warnings.warn(msg)
    if return_dax is True:
        return dnoise, dax
    else:
        return dnoise


def noise_analysis_2d_scannbs(
    data, lamb, phi, mask=None, nxerrbin=None,
    deg=None, knots=None, nbsplines=None, lnbsplines=None,
    nlamb=None, loss=None, max_nfev=None,
    xtol=None, ftol=None, gtol=None,
    method=None, tr_solver=None, tr_options=None,
    verbose=None, plot=None,
    dax=None, fs=None, dmargin=None,
    wintit=None, tit=None, ms=None, sublab=None,
    save_fig=None, name_fig=None, path_fig=None,
    fmt=None, return_dax=None):

    # -------------
    # Check inputs
    if lnbsplines is None:
        lnbsplines = np.arange(5, 21)
    else:
        lnbsplines = np.atleast_1d(lnbsplines).ravel().astype(int)
    if nbsplines is None:
        nbsplines = int(lnbsplines.size/2)
    if nbsplines is not None:
        nbsplines = np.unique(np.atleast_1d(nbsplines)).astype(int)
    nlnbs = lnbsplines.size
    if nxerrbin is None:
        nxerrbin = 100

    if deg is None:
        deg = 2
    if plot is None:
        plot = True
    if verbose is None:
        verbose = 1
    if return_dax is None:
        return_dax = False

    c0 = lamb.shape == phi.shape == data.shape[1:]
    if c0 is not True:
        msg = ("input data, lamb, phi are non-conform!\n"
               + "\t- expected lamb.shape == phi.shape == data.shape[1:]\n"
               + "\t- provided: ")
        raise Exception(msg)

    nspect = data.shape[0]
    domain = {'lamb': {'minmax': [np.nanmin(lamb), np.nanmax(lamb)]},
              'phi': {'minmax': [np.nanmin(phi), np.nanmax(phi)]}}

    if nlamb is None:
        if lamb.ndim == 2:
            nlamb = lamb.shape[0]
        else:
            msg = ("Please provide a value for nlamb (nb of bins)!")
            raise Exception(msg)
    nlamb = int(nlamb)

    # -------------
    # lamb binning
    lambedges = np.linspace(domain['lamb']['minmax'][0],
                            domain['lamb']['minmax'][1], nlamb+1)
    ilamb = np.searchsorted(lambedges, lamb)
    ilambu = np.unique(ilamb)

    # -------------
    # Perform fits
    xdata_edge = np.linspace(0, np.nanmax(data[:, mask]), nxerrbin+1)
    xdata = 0.5*(xdata_edge[1:] + xdata_edge[:-1])
    dataint = np.full((nspect, ilambu.size), np.nan)
    # fit = np.full(data.shape, np.nan)
    indsort = np.zeros((2, phi.size), dtype=int)
    # indout_noeval = np.zeros(phi.shape, dtype=bool)
    chi2n = np.full((nlnbs, nspect, ilambu.size), np.nan)
    chi2_meandata = np.full((nlnbs, nspect, ilambu.size), np.nan)
    const = np.full((nlnbs,), np.nan)
    mean = np.full((nlnbs, nxerrbin), np.nan)
    var = np.full((nlnbs, nxerrbin), np.nan)
    bs_phidata, bs_data, bs_fit, bs_indin = [], [], [], []
    for ii in range(lnbsplines.size):
        nbs = int(lnbsplines[ii])
        # -------------
        # bspline dict and plotting utilities
        dbsplines = multigausfit2d_from_dlines_dbsplines(
            knots=None, deg=deg, nbsplines=nbs,
            phimin=domain['phi']['minmax'][0],
            phimax=domain['phi']['minmax'][1],
            symmetryaxis=False)

        # -------------
        # Perform fits
        if verbose > 0:
            msg = "nbs = {} ({} / {})".format(nbs, ii+1, lnbsplines.size)
            print(msg)
        (fiti, dataint, indsort, indnan, indout_noeval,
         chi2n[ii, ...], chi2_meandata[ii, ...]) = _basic_loop(
             ilambu=ilambu, ilamb=ilamb, phi=phi, data=data, mask=mask,
             domain=domain, nbs=nbs, dbsplines=dbsplines, nspect=nspect,
             method=method, tr_solver=tr_solver, tr_options=tr_options,
             loss=loss, xtol=xtol, ftol=ftol, gtol=gtol,
             max_nfev=max_nfev, verbose=verbose)

        if ii == 0:
            ind_intmax = np.unravel_index(np.argmax(dataint, axis=None),
                                          dataint.shape)

        if nbs in nbsplines:
            isi = np.split(indsort, indnan, axis=1)[ind_intmax[1]]
            bs_phidata.append(phi[isi[0], isi[1]])
            bs_data.append(data[ind_intmax[0], isi[0], isi[1]])
            bs_fit.append(fiti[ind_intmax[0], isi[0], isi[1]])
            indini = ~np.any(np.array([~mask, indout_noeval]), axis=0)
            bs_indin.append(indini[isi[0], isi[1]])

        # -------------
        # Identify outliers with respect to noise model
        (meani, vari, xdatai, consti,
         _, inderrui, _, _) = get_noise_analysis_var_mask(
             fit=fiti, data=data, xdata_edge=xdata_edge,
             mask=(mask & (~indout_noeval)),
             margin=None, valid_fraction=False)

        const[ii] = consti
        mean[ii, inderrui] = meani
        var[ii, inderrui] = vari

    # -------------
    # output dict
    dnoise_scan = {'data': data,
        'chi2n': chi2n, 'chi2_meandata': chi2_meandata, 'dataint': dataint,
        'domain': domain, 'lnbsplines': lnbsplines, 'nbsplines': nbsplines,
        'deg': deg, 'lambedges': lambedges, 'deg': deg,
        'ilamb': ilamb, 'ilambu': ilambu,
        'bs_phidata': bs_phidata, 'bs_data': bs_data,
        'bs_fit': bs_fit, 'bs_indin': bs_indin,
        'var_mean': mean, 'var': var, 'var_xdata': xdata,
        'var_const': const}

    # Plot
    if plot is True:
        try:
            dax = _plot.plot_noise_analysis_scannbs(
                dnoise=dnoise_scan, ms=ms,
                dax=dax, fs=fs, dmargin=dmargin,
                wintit=wintit, tit=tit, sublab=sublab,
                save=save_fig, name=name_fig, path=path_fig, fmt=fmt)
        except Exception as err:
            msg = ("Plotting failed: {}".format(str(err)))
            warnings.warn(msg)

    if return_dax is True:
        return dnoise_scan, dax
    else:
        return dnoise_scan


def get_noise_analysis_var_mask(fit=None, data=None,
                                xdata_edge=None, nxerrbin=None,
                                valid_fraction=None,
                                mask=None, margin=None):
    if margin is None:
        margin = _SIGMA_MARGIN
    if valid_fraction is None:
        valid_fraction = False
    if nxerrbin is None:
        nxerrbin = 100

    err = fit - data
    if mask is None:
        mask = np.ones(err.shape[1:], dtype=bool)
    if xdata_edge is None:
        xdata_edge = np.linspace(0, np.nanmax(fit[:, mask]), nxerrbin)
    inderr = np.searchsorted(xdata_edge[1:-1], fit[:, mask])
    inderru = np.unique(inderr[~np.isnan(err[:, mask])])
    xdata = 0.5*(xdata_edge[1:] + xdata_edge[:-1])[inderru]
    mean = np.full((inderru.size,), np.nan)
    var = np.full((inderru.size,), np.nan)
    nn = np.full((inderru.size,), np.nan)
    for ii in range(inderru.size):
        ind = inderr == inderru[ii]
        indok = ~np.isnan(err[:, mask][ind])
        nn[ii] = np.sum(indok)
        mean[ii] = np.nanmean(err[:, mask][ind])
        var[ii] = nn[ii] * np.nanmean(err[:, mask][ind]**2) / (nn[ii] - 1)

    # fit sqrt on sigma (weight by log10 to take into account diff. nb. of pts)
    const = np.nansum((np.log10(nn)*np.sqrt(var / xdata))
                       / np.nansum(np.log10(nn)))

    # indout
    indok = (~np.isnan(err)) & mask[None, ...]
    indout = np.zeros(err.shape, dtype=bool)
    indout[indok] = (np.abs(err[indok])
                     > margin*const*np.sqrt(np.abs(fit[indok])))
    if valid_fraction is not False:
        indout = np.sum(indout, axis=0)/float(indout.shape[0]) > valid_fraction
    return mean, var, xdata, const, indout, inderru, margin, valid_fraction
