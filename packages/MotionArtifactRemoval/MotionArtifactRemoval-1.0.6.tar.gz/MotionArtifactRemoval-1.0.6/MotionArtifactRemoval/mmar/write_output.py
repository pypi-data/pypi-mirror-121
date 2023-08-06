# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

import os
from PIL import Image
import numpy as np
import SimpleITK as sitk
import tifffile as tiff # we might be able to save tif files using only sitk ...
import matplotlib.pyplot as plt

def write_all_files(output_dir, scan_list, log):
    '''
    Write all output files.  this includes image, mask, bval, and bvec files for all slices, for all scans.

    Parameters:
        output_dir : str
            The path to the base directory.
        scan_list : list
            List of scans.  Each scan is a list of slices, each of which is of type "class multi_frame_slice"
    Return:
        None
    '''
    log.add_msg(f"{os.linesep}modified scans:")

    if not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except OSError as error:
            log.add_msg(f"Could not create output directory: {output_dir} ({error})", is_error_msg=True)

    scan_index = 0
    for scan in scan_list:
        if len(scan_list) == 1:
            scan_dir = ""
        else:
            if scan_index == 0:
                scan_dir = "small_shell"
            elif scan_index == 1:
                scan_dir = "large_shell"
            else:
                scan_dir = f"scan_{scan_index}"
            scan_index += 1
        scan_path = os.path.join(output_dir, scan_dir)
        log.add_msg(" ")
        write_scan_files(scan, scan_path, log)

    excluded_frames_file = os.path.join(output_dir, "excluded_frames.csv")
    write_rejected_frames_file(excluded_frames_file, scan_list)

    return


def write_scan_files(scan, scan_path, log):
    if not os.path.isdir(scan_path):
        try:
            os.mkdir(scan_path)
        except OSError as error:
            log.add_msg(f"Could not create output directory: {scan_path} ({error})", is_error_msg=True)

    slice_index = 0
    for slice in scan:
        slice_dir = "Z"+str(slice_index).zfill(3)
        slice_path = os.path.join(scan_path, slice_dir)
        write_slice(slice, slice_path, log)
        slice_index += 1
    return


def write_slice(slice, slice_path, log):
    if not os.path.isdir(slice_path):
        try:
            os.mkdir(slice_path)
        except OSError as error:
            log.add_msg(f"Could not create output directory: {slice_path} ({error})", is_error_msg=True)

    bval_path = os.path.join(slice_path, "meta.bvals")
    bvec_path = os.path.join(slice_path, "meta.bvecs")
    img_path  = os.path.join(slice_path, "image.tif")
    img_path_nii  = os.path.join(slice_path, "image.nii.gz")
    mask_path  = os.path.join(slice_path, "mask.tif")
    profile_path = os.path.join(slice_path, "profile.jpg")
    write_bval_file(bval_path, slice)
    write_bvec_file(bvec_path, slice)
    write_slice_image_as_tiff(img_path, slice)
    log.add_msg(f"    {img_path_nii}")
    write_slice_image_as_nii(img_path_nii, slice)
    write_slice_mask(mask_path, slice)
    write_profile(profile_path, slice)
    return


def write_bval_file(path, slice):
    '''
    Write a bval file as a tab separated list of floats, with one value per frame.

    Parameters:
        path : str
            The path to the file to write.
        slice : class multi_frame_slice
            The slice to write.
    Return:
        None
    '''

    values = slice.bvals
    if len(slice.rejected):
        r = sorted(slice.rejected, reverse=True)
        for i in r:
            del values[i]
    bval_str = ""
    for v in values:
        bval_str += str(v) + '\t'
    bval_str = bval_str[:-1] + '\n'
    with open(path, 'w') as f:
        f.write(bval_str)
    return


def write_bvec_file(path, slice):
    '''
    Write a bvec file as a tab separated list of floats.  For each frame there is a vector, (x, y, z) value.
    The list of vectors is saved with the coordinates separated - a separate list for each coordinate, in the order
    x, y, z.

    Parameters:
        path : str
            The path to the file to write.
        slice : class multi_frame_slice
            The slice to write.
    Return:
        None
    '''
    values = slice.bvecs
    if len(slice.rejected):
        r = sorted(slice.rejected, reverse=True)
        for i in r:
            del values[i]
    x_str = ""
    y_str = ""
    z_str = ""
    for v in values:
        x_str += str(v[0]) + '\t'
        y_str += str(v[1]) + '\t'
        z_str += str(v[2]) + '\t'
    x_str = x_str[:-1] + '\n'
    y_str = y_str[:-1] + '\n'
    z_str = z_str[:-1] + '\n'
    with open(path, 'w') as f:
        f.write(x_str + y_str + z_str)
    return


def write_slice_image_as_tiff(path, slice):
    '''    
    Write a slice to a file.
        
    Parameters
    ----------
    path : str
        The path to the file to write.
    slice : class multi_frame_slice
        The slice to write.
    
    Returns
    -------
    None

    '''
    img = slice.img
    if slice.rejected:
        img = np.delete(img, slice.rejected, 0)
    tiff.imsave(path, img)
    return

def write_slice_image_as_nii(path, slice):
    '''
    Write a slice to a file.

    Parameters
    ----------
    path : str
        The path to the file to write.
    slice : class multi_frame_slice
        The slice to write.

    Returns
    -------
    None

    '''
    img = slice.img
    img_itk = sitk.GetImageFromArray(img)
    sitk.WriteImage(img_itk, path)



def write_slice_mask(path, slice):
    '''
    Write a mask file for a given slice.
    
    Parameters
    ----------
    path : str
        The path to the mask file to be written.
    slice : class multi_frame_slice
        The slice to write the mask for.
    
    Returns
    -------
    None

    '''
    if type(slice.mask) == type(None):
        return
    tiff.imsave(path, slice.mask)
    return




def write_rejected_frames_file(output_file, scan_list):
    '''
    Write the list of rejected frames.

    Parameters:
        output_dir : str
            The path to the directory in which to write the file.
        scan_list : list
            List of scans.  Each scan is a list of slices, each of which is of type "class multi_frame_slice"
    Return:
        None
    '''
    body = "scan, slice, excluded_frames\n"

    for scan_index in range(len(scan_list)):
        scan = scan_list[scan_index]
        for z in range(len(scan)):
            slice = scan[z]
            body += f"{scan_index}, {z}"
            for n in slice.rejected:
                body += f", {n}"
            body += "\n"
    with open(output_file, 'w') as f:
        f.write(body)

    return


def write_profile(file_path, slice):
    '''
    Write the profile of the foreground and background of the specified slice.

    Parameters:
        path : str
            The path to the image file to write.
        slice : class multi_frame_slice
            Profiles of the fg and bg of this slice are generated.
    Return:
        None
    '''

    if type(slice.profile_foreground) == type(None):
        return
    nf = len(slice.profile_foreground)
    x1 = np.linspace(1,nf, num=nf-1)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x1, slice.profile_foreground[1:], 'g-')
    ax2.plot(x1, slice.profile_background[1:], 'b-')
    ax1.set_xlabel('slice number')
    ax1.set_ylabel('foreground intensity', color='g')
    ax2.set_ylabel('background intensity', color='b')
    plt.savefig(file_path)
    plt.close()


