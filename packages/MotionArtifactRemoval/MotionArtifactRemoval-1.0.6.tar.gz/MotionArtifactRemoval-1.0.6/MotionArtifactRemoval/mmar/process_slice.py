# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

import numpy as np

from .create_mask import create_mask

def find_bad_frames(slice, fg_thresh, bg_thresh):
    '''
    Finds the bad frames in a slice.

    Parameters
    ----------
    slice : Slice
        The slice to be processed.

    Returns
    -------
    mask : ndarray
        A boolean array of the same shape as the image.
    slice : Slice
        The modified slice
    '''
    image = slice.img
    bvals = slice.bvals
    bvecs = slice.bvecs
    mask, _ = create_mask(image[0,:,:], fg=False)

    nz = slice.img.shape[0]
    profile_foreground = np.zeros(nz)
    profile_background = np.zeros(nz)
    for iz in range(nz):
        profile_foreground[iz] = np.sum(slice.img[iz,:,:] * (1-mask)) / np.sum((1-mask))
        profile_background[iz] = np.sum(slice.img[iz,:,:] * (mask)) / np.sum((mask))

    slice.mask = mask
    slice.profile_background = profile_background
    slice.profile_foreground = profile_foreground

    e_fg = get_outliers(profile_background, mode='MAD', MAD_thr=fg_thresh)
    e_bg = get_outliers(profile_foreground, mode='MAD', MAD_thr=bg_thresh)
    for n in e_bg:
        if not n in e_fg:
            e_fg.append(n)
    slice.rejected = sorted(e_fg, reverse=False)

    return slice




def get_outliers(data, mode='MAD', r=None, MAD_thr=None):
    '''
    This function identifies outliers in a given dataset.

    Parameters
    ----------
    data : list
        A list of numbers.
    mode : str, optional
        The method used to identify outliers.
        'std' uses standard deviation method.
        'MAD' uses median absolute deviation method.
        The default is 'MAD'.
    r : float, optional
        The ratio used to identify outliers.
        The default is None.
    MAD_thr : float, optional
        The threshold used to identify outliers using median absolute deviation method.
        The default is None, however in [https://www.sciencedirect.com/science/article/abs/pii/S0022103113000668]
        it has been suggested to use 2.5

    Returns
    -------
    outliers : list
        A list of indices of outliers in the given dataset.

    '''
    if mode=='std':
        mean = np.mean(data)
        std = np.std(data)
        outliers = []
        for i in range(1,len(data)):
            if data[i] > mean + r*std or data[i] < mean - r*std:
                outliers.append(i)
    elif mode=='MAD':
        # calculate median and median absolute deviation
        # ref: https://www.sciencedirect.com/science/article/abs/pii/S0022103113000668
        data_median = np.median(data)
        data_mad = np.median([np.abs(data - data_median)])
        # identify outliers
        cut_off = data_mad * MAD_thr
        lower, upper = data_median - cut_off, data_median + cut_off
        outliers = []
        for i in range(1,len(data)):
            if data[i] < lower or data[i] > upper:
                outliers.append(i)
    return outliers

