# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module provides tools for detecting sources in an image.
"""

from copy import deepcopy
import warnings

from astropy.convolution import convolve, Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma, SigmaClip
from astropy.utils.decorators import deprecated, deprecated_renamed_argument
from astropy.utils.exceptions import AstropyUserWarning
import numpy as np

from .core import SegmentationImage
from .utils import _make_binary_structure
from ..utils._stats import nanmean, nanstd
from ..utils.exceptions import NoDetectionsWarning

__all__ = ['detect_threshold', 'detect_sources', 'make_source_mask']


@deprecated_renamed_argument('mask_value', None, '1.4',
                             alternative='mask')
@deprecated_renamed_argument('sigclip_sigma', None, '1.5',
                             alternative='sigma_clip')
@deprecated_renamed_argument('sigclip_iters', None, '1.5',
                             alternative='sigma_clip')
def detect_threshold(data, nsigma, background=None, error=None, mask=None,
                     mask_value=None, sigclip_sigma=3.0, sigclip_iters=10,
                     sigma_clip=SigmaClip(sigma=3.0, maxiters=10)):
    """
    Calculate a pixel-wise threshold image that can be used to detect
    sources.

    This is a simple convenience function that uses sigma-clipped
    statistics to compute a scalar background and noise estimate. In
    general, one should perform more sophisticated estimates, e.g.,
    using `~photutils.background.Background2D`.

    Parameters
    ----------
    data : 2D `~numpy.ndarray`
        The 2D array of the image.

    nsigma : float
        The number of standard deviations per pixel above the
        ``background`` for which to consider a pixel as possibly being
        part of a source.

    background : float or 2D `~numpy.ndarray`, optional
        The background value(s) of the input ``data``. ``background``
        may either be a scalar value or a 2D array with the same
        shape as the input ``data``. If the input ``data`` has been
        background-subtracted, then set ``background`` to ``0.0`` (this
        should be typical). If `None`, then a scalar background value
        will be estimated as the sigma-clipped image mean.

    error : float or 2D `~numpy.ndarray`, optional
        The Gaussian 1-sigma standard deviation of the background
        noise in ``data``. ``error`` should include all sources of
        "background" error, but *exclude* the Poisson error of the
        sources. If ``error`` is a 2D image, then it should represent
        the 1-sigma background error in each pixel of ``data``. If
        `None`, then a scalar background rms value will be estimated
        as the sigma-clipped image standard deviation.

    mask : 2D bool `~numpy.ndarray`, optional
        A boolean mask with the same shape as ``data``, where a `True`
        value indicates the corresponding element of ``data`` is masked.
        Masked pixels are ignored when computing the image background
        statistics.

    mask_value : float, optional
        Deprecated.
        An image data value (e.g., ``0.0``) that is ignored when
        computing the image background statistics.  ``mask_value`` will
        be ignored if ``mask`` is input.

    sigclip_sigma : float, optional
        Deprecated (use the ``sigma_clip`` keyword).
        The number of standard deviations to use as the clipping limit
        when calculating the image background statistics.

    sigclip_iters : int, optional
        Deprecated (use the ``sigma_clip`` keyword).
        The maximum number of iterations to perform sigma clipping, or
        `None` to clip until convergence is achieved (i.e., continue
        until the last iteration clips nothing) when calculating the
        image background statistics.

    sigma_clip : `astropy.stats.SigmaClip` instance, optional
        A `~astropy.stats.SigmaClip` object that defines the sigma
        clipping parameters.

    Returns
    -------
    threshold : 2D `~numpy.ndarray`
        A 2D image with the same shape as ``data`` containing the
        pixel-wise threshold values.

    See Also
    --------
    :class:`photutils.background.Background2D`
    :func:`photutils.segmentation.detect_sources`
    :class:`photutils.segmentation.SourceFinder`

    Notes
    -----
    The ``mask``, ``mask_value`` (deprecated), ``sigclip_sigma``
    (deprecated), ``sigclip_iters`` (deprecated), and ``sigma_clip``
    inputs are used only if it is necessary to estimate ``background``
    or ``error`` using sigma-clipped background statistics. If
    ``background`` and ``error`` are both input, then ``mask``,
    ``mask_value``, ``sigclip_sigma``, ``sigclip_iters``, and
    ``sigma_clip`` are ignored.

    The deprecated ``sigclip_sigma`` and ``sigclip_iters`` keywords
    should not be used with the ``sigma_clip`` keyword. If they are,
    then their values will override the corresponding ``sigma_clip``
    values.
    """
    if not isinstance(sigma_clip, SigmaClip):
        raise TypeError('sigma_clip must be a SigmaClip object')

    if sigclip_sigma != sigma_clip.sigma:
        sigma_clip = deepcopy(sigma_clip)
        sigma_clip.sigma = sigclip_sigma
    if sigclip_iters != sigma_clip.maxiters:
        sigma_clip = deepcopy(sigma_clip)
        sigma_clip.maxiters = sigclip_iters

    if background is None or error is None:
        if mask is not None:
            data = np.ma.MaskedArray(data, mask)
        if mask_value is not None:
            data = np.ma.masked_values(data, mask_value)

        clipped_data = sigma_clip(data, masked=False, return_bounds=False,
                                  copy=True)

    if background is None:
        background = nanmean(clipped_data)
    if not np.isscalar(background) and background.shape != data.shape:
        raise ValueError('If input background is 2D, then it must have the '
                         'same shape as the input data.')

    if error is None:
        error = nanstd(clipped_data)
    if not np.isscalar(error) and error.shape != data.shape:
        raise ValueError('If input error is 2D, then it must have the same '
                         'shape as the input data.')

    return (np.broadcast_to(background, data.shape)
            + np.broadcast_to(error * nsigma, data.shape))


def _detect_sources(data, thresholds, npixels, *, kernel=None, connectivity=8,
                    selem=None, inverse_mask=None, deblend_skip=False):
    """
    Detect sources above a specified threshold value in an image.

    Detected sources must have ``npixels`` connected pixels that are
    each greater than the ``threshold`` value.  If the filtering option
    is used, then the ``threshold`` is applied to the filtered image.
    The input ``mask`` can be used to mask pixels in the input data.
    Masked pixels will not be included in any source.

    This function does not deblend overlapping sources.  First use this
    function to detect sources followed by
    :func:`~photutils.segmentation.deblend_sources` to deblend sources.

    Parameters
    ----------
    data : 2D `~numpy.ndarray`
        The 2D array of the image.

        .. note::
           It is recommended that the user convolve the data with
           ``kernel`` and input the convolved data directly into the
           ``data`` parameter. In this case do not input a ``kernel``,
           otherwise the data will be convolved twice.

    thresholds : 2D `~numpy.ndarray` or 1D array of floats
        The data values (as a 1D array of floats) or pixel-wise
        data values to be used for the detection thresholds. A 2D
        ``threshold`` must have the same shape as ``data``.

    npixels : int
        The number of connected pixels, each greater than ``threshold``,
        that an object must have to be detected. ``npixels`` must be a
        positive integer.

    kernel : 2D `~numpy.ndarray` or `~astropy.convolution.Kernel2D`, optional
        The 2D array of the kernel used to filter the image before
        thresholding. Filtering the image will smooth the noise and
        maximize detectability of objects with a shape similar to the
        kernel. ``kernel`` must be `None` if the input ``data`` are
        already convolved.

    connectivity : {4, 8}, optional
        The type of pixel connectivity used in determining how pixels
        are grouped into a detected source. The options are 4 or
        8 (default). 4-connected pixels touch along their edges.
        8-connected pixels touch along their edges or corners. For
        reference, SourceExtractor uses 8-connected pixels.

    mask : 2D bool `~numpy.ndarray`, optional
        A boolean mask, with the same shape as the input ``data``, where
        `True` values indicate masked pixels. Masked pixels will not be
        included in any source.

    deblend_skip : bool, optional
        If `True` do not include the segmentation image in the output
        list for any threshold level where the number of detected
        sources is less than 2. This is useful for source deblending and
        improves its performance.

    Returns
    -------
    segment_image : list of `~photutils.segmentation.SegmentationImage`
        A list of 2D segmentation images, with the same shape as
        ``data``, where sources are marked by different positive integer
        values. A value of zero is reserved for the background. If
        no sources are found for a given threshold, then the output
        list will contain `None` for that threshold. Also see the
        ``deblend_skip`` keyword.
    """
    from scipy.ndimage import label as ndi_label
    from scipy.ndimage import find_objects

    segms = []
    for threshold in thresholds:
        # ignore RuntimeWarning caused by > comparison when data contains NaNs
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            segment_img = data > threshold

        if inverse_mask is not None:
            segment_img &= inverse_mask

        # return if threshold was too high to detect any sources
        if np.count_nonzero(segment_img) == 0:
            warnings.warn('No sources were found.', NoDetectionsWarning)
            if not deblend_skip:
                segms.append(None)
            continue

        # this is faster than recasting segment_img to int and using
        # output=segment_img
        segment_img, nlabels = ndi_label(segment_img, structure=selem)
        labels = np.arange(nlabels) + 1

        # remove objects with less than npixels
        # NOTE: making cutout images and setting their pixels to 0 is
        # ~10x faster than using segment_img directly and ~2x faster
        # than using ndimage.sum_labels.
        slices = find_objects(segment_img)
        segm_labels = []
        segm_slices = []
        for label, slc in zip(labels, slices):
            cutout = segment_img[slc]
            segment_mask = (cutout == label)
            if np.count_nonzero(segment_mask) < npixels:
                cutout[segment_mask] = 0
            else:
                segm_labels.append(label)
                segm_slices.append(slc)

        if np.count_nonzero(segment_img) == 0:
            warnings.warn('No sources were found.', NoDetectionsWarning)
            if not deblend_skip:
                segms.append(None)
            continue

        # relabel the segmentation image with consecutive numbers
        nlabels = len(segm_labels)
        if len(labels) != nlabels:
            label_map = np.zeros(np.max(labels) + 1, dtype=int)
            labels = np.arange(nlabels) + 1
            label_map[segm_labels] = labels
            segment_img = label_map[segment_img]

        segm = object.__new__(SegmentationImage)
        segm._data = segment_img
        segm.__dict__['labels'] = labels
        segm.__dict__['slices'] = segm_slices

        if deblend_skip and segm.nlabels == 1:
            continue

        segms.append(segm)

    return segms


def detect_sources(data, threshold, npixels, kernel=None, connectivity=8,
                   mask=None):
    """
    Detect sources above a specified threshold value in an image.

    Detected sources must have ``npixels`` connected pixels that are
    each greater than the ``threshold`` value.  If the filtering option
    is used, then the ``threshold`` is applied to the filtered image.
    The input ``mask`` can be used to mask pixels in the input data.
    Masked pixels will not be included in any source.

    This function does not deblend overlapping sources.  First use this
    function to detect sources followed by
    :func:`~photutils.segmentation.deblend_sources` to deblend sources.

    Parameters
    ----------
    data : 2D `~numpy.ndarray`
        The 2D array of the image.

        .. note::
           It is recommended that the user convolve the data with
           ``kernel`` and input the convolved data directly into the
           ``data`` parameter. In this case do not input a ``kernel``,
           otherwise the data will be convolved twice.

    threshold : float or 2D `~numpy.ndarray`
        The data value or pixel-wise data values to be used for the
        detection threshold. A 2D ``threshold`` array must have the same
        shape as ``data``.

    npixels : int
        The number of connected pixels, each greater than ``threshold``,
        that an object must have to be detected. ``npixels`` must be a
        positive integer.

    kernel : 2D `~numpy.ndarray` or `~astropy.convolution.Kernel2D`, optional
        The 2D array of the kernel used to filter the image before
        thresholding. Filtering the image will smooth the noise and
        maximize detectability of objects with a shape similar to the
        kernel. ``kernel`` must be `None` if the input ``data`` are
        already convolved.

    connectivity : {4, 8}, optional
        The type of pixel connectivity used in determining how pixels
        are grouped into a detected source. The options are 4 or
        8 (default). 4-connected pixels touch along their edges.
        8-connected pixels touch along their edges or corners. For
        reference, SourceExtractor uses 8-connected pixels.

    mask : 2D bool `~numpy.ndarray`, optional
        A boolean mask, with the same shape as the input ``data``, where
        `True` values indicate masked pixels. Masked pixels will not be
        included in any source.

    Returns
    -------
    segment_image : `~photutils.segmentation.SegmentationImage` or `None`
        A 2D segmentation image, with the same shape as ``data``, where
        sources are marked by different positive integer values. A value
        of zero is reserved for the background. If no sources are found
        then `None` is returned.

    See Also
    --------
    :func:`photutils.segmentation.deblend_sources`
    :class:`photutils.segmentation.SourceFinder`

    Examples
    --------
    .. plot::
        :include-source:

        from astropy.convolution import convolve
        from astropy.stats import sigma_clipped_stats
        from astropy.visualization import simple_norm
        import matplotlib.pyplot as plt
        from photutils.datasets import make_100gaussians_image
        from photutils.segmentation import (detect_threshold, detect_sources,
                                            make_2dgaussian_kernel)

        # make a simulated image
        data = make_100gaussians_image()

        # use sigma-clipped statistics to (roughly) estimate the background
        # background noise levels
        mean, _, std = sigma_clipped_stats(data)

        # subtract the background
        data -= mean

        # detect the sources
        threshold = 3. * std
        kernel = make_2dgaussian_kernel(3.0, size=3)  # FWHM = 3.
        convolved_data = convolve(data, kernel)
        segm = detect_sources(convolved_data, threshold, npixels=5)

        # plot the image and the segmentation image
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
        norm = simple_norm(data, 'sqrt', percent=99.)
        ax1.imshow(data, origin='lower', interpolation='nearest',
                   norm=norm)
        ax2.imshow(segm.data, origin='lower', interpolation='nearest',
                   cmap=segm.make_cmap(seed=1234))
        plt.tight_layout()
    """
    if (npixels <= 0) or (int(npixels) != npixels):
        raise ValueError('npixels must be a positive integer, got '
                         f'"{npixels}"')

    if mask is not None:
        if mask.shape != data.shape:
            raise ValueError('mask must have the same shape as the input '
                             'image.')
        if mask.all():
            raise ValueError('mask must not be True for every pixel. There '
                             'are no unmasked pixels in the image to detect '
                             'sources.')
        inverse_mask = np.logical_not(mask)
    else:
        inverse_mask = None

    if kernel is not None:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', AstropyUserWarning)
            data = convolve(data, kernel, mask=mask, normalize_kernel=True)

    selem = _make_binary_structure(data.ndim, connectivity)

    return _detect_sources(data, (threshold,), npixels, kernel=kernel,
                           connectivity=connectivity, selem=selem,
                           inverse_mask=inverse_mask)[0]


@deprecated('1.5.0', alternative='SegmentationImage.make_source_mask')
@deprecated_renamed_argument('filter_fwhm', None, '1.4', message='Use the '
                             'kernel keyword')
@deprecated_renamed_argument('filter_size', None, '1.4', message='Use the '
                             'kernel keyword')
def make_source_mask(data, nsigma, npixels, mask=None, filter_fwhm=None,
                     filter_size=3, kernel=None, sigclip_sigma=3.0,
                     sigclip_iters=5, dilate_size=11):
    """
    Make a source mask using source segmentation and binary dilation.

    Parameters
    ----------
    data : 2D `~numpy.ndarray`
        The 2D array of the image.

        .. note::
           It is recommended that the user convolve the data with
           ``kernel`` and input the convolved data directly into the
           ``data`` parameter. In this case do not input a ``kernel``
           (or ``filter_fwhm``, ``filter_size``; deprecated), otherwise
           the data will be convolved twice.

    nsigma : float
        The number of standard deviations per pixel above the
        ``background`` for which to consider a pixel as possibly being
        part of a source.

    npixels : int
        The number of connected pixels, each greater than ``threshold``,
        that an object must have to be detected.  ``npixels`` must be a
        positive integer.

    mask : 2D bool `~numpy.ndarray`, optional
        A boolean mask with the same shape as ``data``, where a `True`
        value indicates the corresponding element of ``data`` is masked.
        Masked pixels are ignored when computing the image background
        statistics.

    filter_fwhm : float, optional
        Deprecated (use the ``kernel`` keyword).
        The full-width at half-maximum (FWHM) of the Gaussian kernel
        to filter the image before thresholding. ``filter_fwhm``
        and ``filter_size`` are ignored if ``kernel`` is defined.
        ``filter_fwhm`` must be `None` if the input ``data`` are already
        convolved.

    filter_size : float, optional
        Deprecated (use the ``kernel`` keyword).
        The size of the square Gaussian kernel image. Used only if
        ``filter_fwhm`` is defined. ``filter_fwhm`` and ``filter_size``
        are ignored if ``kernel`` is defined. ``filter_size`` must be
        `None` if the input ``data`` are already convolved.

    kernel : 2D `~numpy.ndarray` or `~astropy.convolution.Kernel2D`, optional
        The 2D array of the kernel used to filter the image before
        thresholding. Filtering the image will smooth the noise
        and maximize detectability of objects with a shape similar
        to the kernel. ``kernel`` overrides ``filter_fwhm`` and
        ``filter_size``. ``kernel`` must be `None` if the input ``data``
        are already convolved.

    sigclip_sigma : float, optional
        The number of standard deviations to use as the clipping limit
        when calculating the image background statistics.

    sigclip_iters : int, optional
        The maximum number of iterations to perform sigma clipping, or
        `None` to clip until convergence is achieved (i.e., continue
        until the last iteration clips nothing) when calculating the
        image background statistics.

    dilate_size : int, optional
        The size of the square array used to dilate the segmentation
        image.

    Returns
    -------
    mask : 2D bool `~numpy.ndarray`
        A 2D boolean image containing the source mask.
    """
    from scipy import ndimage

    sigma_clip = SigmaClip(sigma=sigclip_sigma, maxiters=sigclip_iters)
    threshold = detect_threshold(data, nsigma, background=None, error=None,
                                 mask=mask, sigma_clip=sigma_clip)

    if kernel is None and filter_fwhm is not None:
        kernel_sigma = filter_fwhm * gaussian_fwhm_to_sigma
        kernel = Gaussian2DKernel(kernel_sigma, x_size=filter_size,
                                  y_size=filter_size)
    if kernel is not None:
        kernel.normalize()

    segm = detect_sources(data, threshold, npixels, kernel=kernel)
    if segm is None:
        return np.zeros(data.shape, dtype=bool)

    selem = np.ones((dilate_size, dilate_size))
    return ndimage.binary_dilation(segm.data.astype(bool), selem)
