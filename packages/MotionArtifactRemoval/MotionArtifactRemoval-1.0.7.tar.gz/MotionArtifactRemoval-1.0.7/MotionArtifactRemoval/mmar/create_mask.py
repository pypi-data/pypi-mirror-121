# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

import numpy as np
from scipy import ndimage
from skimage.filters import threshold_triangle, threshold_otsu
from skimage.morphology import binary_closing
from skimage.measure import label

def create_mask(image, threshold_algo='triangle_otsu', threshold=None, fg=True):
    """
    Estimates the background and pixel intesnity background theshold for an
    image. Note intensity is calculated using skimage.color.rgb2grey
    Parameters
    ----------
    image: array-like, (height, width)
        Image from which the mask is created.
    threshold_algo: str, ['otsu', 'triangle', 'triangle_otsu']
        Thresholding algorithm to estimate the background.
        'otsu': skimage.filters.threshold_otsu
        'triangle': skimage.filters.threshold_triangle
        'triangle_otsu': .9 * triangle + .1 * otsu
    threshold: None, float, int
        User provided threshold. If None, will be estimated using one
        of the thresholding algorithms.
    Output
    ------
    background_mask, thresholded first frame
    background_mask: array-like, (height, width)
        The True/False mask of estimated background pixels.
    threshold: float
        The lower-bound backgound threshold, or upper-bound foreground intensity for the image.
    """

    if threshold is None:
        if threshold_algo == 'otsu':
            threshold = threshold_otsu(image)

        elif threshold_algo == 'triangle':
            threshold = threshold_triangle(image)

        elif threshold_algo == 'triangle_otsu':
            triangle = threshold_triangle(image)
            otsu = threshold_otsu(image)

            threshold = .9 * triangle + .1 * otsu

        else:
            raise ValueError('threshold_algo = {} is invalid argument'.format(threshold_algo))
    if fg:
        mask = image < threshold
    else:
        mask = image > threshold

    refined_mask = get_largest_island(close_and_fill(mask))
    
    return refined_mask, threshold



def close_and_fill(image):
    '''
    This function closes and fills a binary image.
    
    Parameters
    ----------
    image : numpy.ndarray
        A binary image.
        
    Returns
    -------
    numpy.ndarray
        A binary image.
    '''
    return ndimage.binary_fill_holes(binary_closing(image))

def get_largest_island(binary_image):
    labeled_image, num_features = label(binary_image,return_num=True)
    max_area = 0
    max_label = 0
    for i in range(1, num_features + 1):
        area = np.sum(labeled_image == i)
        if area > max_area:
            max_area = area
            max_label = i
    return (labeled_image == max_label)