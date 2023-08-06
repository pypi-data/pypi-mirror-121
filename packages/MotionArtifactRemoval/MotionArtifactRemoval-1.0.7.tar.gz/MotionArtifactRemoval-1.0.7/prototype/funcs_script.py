from skimage.color import rgb2gray
from skimage.filters import threshold_triangle, threshold_otsu
from skimage.morphology import binary_closing
from scipy import ndimage
import SimpleITK as sitk
import numpy as np

def bg_estimation(f_path, threshold_algo='triangle_otsu'):
    '''
    Estimates the background and foreground intensities of a stack of images.
    The background is estimated using a thresholding algorithm, and the foreground is whatever that remains.
    
    Parameters
    ----------
    f_path : str
        Path to the image stack file.
    threshold_algo : str, optional
        Thresholding algorithm to use. Options are ['otsu', 'triangle', 'triangle_otsu'].
        The default is 'triangle_otsu'.
    
    Returns
    -------
    normalized_fg : ndarray (frames, slices)
        Average intensities of the forground 

    background_fg : ndarray (frames, slices)
        Average intensities of the background 

    '''
    # Read image from path file
    img_stack = sitk.GetArrayFromImage(sitk.ReadImage(f_path))

    # threshold to separate foreground and background
    frames, slices, height, width = img_stack.shape
    bg_mask = np.zeros_like(img_stack)
    threshold = np.zeros_like(img_stack)
    for ifr in range(frames):
        for iz in range(slices):
            bg_mask[ifr, iz,:,:], threshold[ifr, iz,:,:] = estimate_background(img_stack[ifr, iz,:,:], threshold_algo=threshold_algo)


    normalized_fg = np.zeros((frames, slices))
    normalized_bg = np.zeros((frames, slices))
    for ifr in range(frames):
        for iz in range(slices):
            normalized_bg[ifr, iz] = np.sum(img_stack[ifr, iz,:,:] * (1-bg_mask[ifr, iz,:,:])) / np.sum((1-bg_mask[ifr, iz,:,:]))
            normalized_fg[ifr, iz] = np.sum(img_stack[ifr, iz,:,:] * (bg_mask[ifr, iz,:,:])) / np.sum((bg_mask[ifr, iz,:,:]))
    return normalized_fg, normalized_bg

def estimate_background(image, threshold_algo='triangle_otsu',
                        threshold=None):
    """
    Estimates the background and pixel intesnity background theshold for an
    image. Note intensity is calculated using skimage.color.rgb2grey
    Parameters
    ----------
    image: array-like, (height, width, n_channels)
        Image whose background to estimate.
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
    background_mask, threshold
    background_mask: array-like, (height, width)
        The True/False mask of estimated background pixels.
    threshold: float
        The (lower bound) backgound threshold intensity for the image.
    """

    grayscale_image = rgb2gray(image)

    if threshold is None:
        if threshold_algo == 'otsu':
            threshold = threshold_otsu(grayscale_image)

        elif threshold_algo == 'triangle':
            threshold = threshold_triangle(grayscale_image)

        elif threshold_algo == 'triangle_otsu':
            triangle = threshold_triangle(grayscale_image)
            otsu = threshold_otsu(grayscale_image)

            threshold = .9 * triangle + .1 * otsu

        else:
            raise ValueError('threshold_algo = {} is invalid argument'.\
                  format(threshold_algo))

    background_mask = grayscale_image > threshold

    return close_and_fill(background_mask), threshold

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
