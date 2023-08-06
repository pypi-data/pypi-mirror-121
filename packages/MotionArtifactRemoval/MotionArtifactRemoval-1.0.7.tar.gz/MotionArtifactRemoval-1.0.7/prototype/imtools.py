import ipywidgets as ipyw
from skimage.color import rgb2gray
from skimage.filters import threshold_triangle, threshold_otsu
from skimage.morphology import binary_closing
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

def norm_im(data):
    '''
    normalizes 2d array to [0, 1]
    '''
    return (data - np.min(data)) / (np.max(data) - np.min(data))

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
    this function closes and fills a binary image
    '''
    return ndimage.binary_fill_holes(binary_closing(image))


class ImageSliceViewer3D:
    """ 
    ImageSliceViewer3D is for viewing volumetric image slices in jupyter or
    ipython notebooks. 
    
    User can interactively change the slice plane selection for the image and 
    the slice plane being viewed. 

    Argumentss:
    Volume = 3D input image
    figsize = default(8,8), to set the size of the figure
    cmap = default('plasma'), string for the matplotlib colormap. You can find 
    more matplotlib colormaps on the following link:
    https://matplotlib.org/users/colormaps.html
    
    """
    
    def __init__(self, volume, figsize=(8,8), cmap='plasma'):
        self.volume = volume
        self.figsize = figsize
        self.cmap = cmap
        self.v = [np.min(volume), np.max(volume)]
        
        # Call to select slice plane
        ipyw.interact(self.view_selection, view=ipyw.RadioButtons(
            options=['x-y','y-z', 'z-x'], value='y-z', 
            description='Slice plane selection:', disabled=False,
            style={'description_width': 'initial'}))
    
    def view_selection(self, view):
        # Transpose the volume to orient according to the slice plane selection
        orient = {"y-z":[1,2,0], "z-x":[2,0,1], "x-y": [0,1,2]}
        self.vol = np.transpose(self.volume, orient[view])
        maxZ = self.vol.shape[2] - 1
        
        # Call to view a slice within the selected slice plane
        ipyw.interact(self.plot_slice, 
            z=ipyw.IntSlider(min=0, max=maxZ, step=1, continuous_update=False, 
            description='Image Slice:'))
        
    def plot_slice(self, z):
        # Plot slice for the given plane and slice
        self.fig = plt.figure(figsize=self.figsize)
        plt.imshow(self.vol[:,:,z], cmap=plt.get_cmap(self.cmap), 
            vmin=self.v[0], vmax=self.v[1])
