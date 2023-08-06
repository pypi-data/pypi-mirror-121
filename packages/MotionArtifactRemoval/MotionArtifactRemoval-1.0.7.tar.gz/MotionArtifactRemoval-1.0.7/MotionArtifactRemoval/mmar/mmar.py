#!/usr/bin/env python

# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

'''
This script

To Do:
    - catch possible exception when bval and bvec file entries are converted to numbers
    - catch exceptions when writing output files
    - check for directory separators in log file name

'''
import sys
import os
import numpy as np
import SimpleITK as sitk
import csv

from process_slice import find_bad_frames
from write_output import write_all_files
from command_line_params import command_line_params
from message_log import message_log


'''
import ipywidgets as ipyw
from IPython.display import set_matplotlib_formats
import pandas as pd
'''


class multi_frame_slice:
    img = None
    mask = None
    bvals = None
    bvecs = None
    rejected = None
    profile_background = None
    profile_foreground = None

def main():
    '''
    '''

    #
    # Parse the command line parameters
    #
    p = command_line_params()
    p.check_parameters()
    log = message_log(p.verbose)
    log.add_msg(p.params_message())

    #
    # Open the input files
    #
    bval_list = open_bval_file(p.bvals_path, log)
    bvec_list = open_bvec_file(p.bvecs_path, log)
    img = sitk.GetArrayFromImage(sitk.ReadImage(p.scan_path))

    #
    # Count the number of sequences
    #
    thresh = p.bval_thresh
    frame_starts = []
    for i in range(len(bval_list)):
        if bval_list[i] < thresh:
            frame_starts.append(i)

    frames, slices, height, width = img.shape
    log.add_msg(f"    sequences = {len(frame_starts)}")
    log.add_msg(f"    width = {width}")
    log.add_msg(f"    height = {height}")
    log.add_msg(f"    slices = {slices}")
    log.add_msg(f"    frames = {frames}")
    if not ((frames == len(bval_list)) and (frames == len(bvec_list))):
        log.add_msg("input files do not match in frame count", is_error_msg=True)
        exit(-1)

    #
    # Separate scans
    #
    frame_starts.append(len(bval_list))
    scan_list = []
    for i in range(len(frame_starts)-1):
        bvals = bval_list[frame_starts[i]: frame_starts[i+1]]
        bvecs = bvec_list[frame_starts[i]: frame_starts[i+1]]
        slice_list = []
        for z in range(slices):
            s = multi_frame_slice()
            s.img = img[frame_starts[i]:frame_starts[i+1], z, :, :]
            s.bvals = bvals.copy()
            s.bvecs = bvecs.copy()
            s.rejected = []
            slice_list.append(s)
        scan_list.append(slice_list)
    img = None
    bval_list = None
    bvec_list = None
    frame_starts = None

    #
    # Read the rejected frame file, if specified
    #
    if p.rejected_frames_file:
        if not os.path.isfile(p.rejected_frames_file):
            log.add_msg(f"rejected frames file does not exist: {p.rejected_frames_file}", is_error_msg=True)
            exit(-1)

        lines = []
        with open(p.rejected_frames_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            lines = list(reader)
        for l in lines:
            if not l[0].isnumeric():
                continue
            n_scan = int(l[0])
            if n_scan < 0 or n_scan >= len(scan_list):
                continue;
            if not l[1].isnumeric():
                continue
            n_slice = int(l[1])
            if n_slice < 0 or n_slice >= len(scan_list[n_scan]):
                continue

            for f in l[2:]:
                if not f.isnumeric():
                    continue
                n_frame = int(f)
                if n_frame < 0 or n_frame >= frames:
                    continue
                scan_list[n_scan][n_slice].rejected.append(n_frame)

    #
    # Loop over all scans and through all slices, processing images
    #
    #     scan = scan_list[n]
    #     slice = scan[z]
    #     image = slice.img
    #     bvals = slice.bvals
    #     bvecs = slice.bvecs
    #
    if not p.rejected_frames_file:
        scan_processed = []
        for i in range(len(scan_list)):
            if i == 0:
                scan_name = "small_shell"
            elif i == 1:
                scan_name = "large_shell"
            else:
                scan_name = f"scan_{scan_index}"
            log.add_msg(f"{os.linesep}scan: {scan_name}")
            slice_processed = []
            for z in range(len(scan_list[i])):
                slice_processed.append(find_bad_frames(scan_list[i][z], p.fg_thresh, p.bg_thresh))
                log.add_msg(f"    slice {z}: {slice_processed[-1].rejected}")
            scan_processed.append(slice_processed)
    
    #
    # Write output files
    #
    write_all_files(p.output_dir, scan_list, log)
    log.save_log(p.log_file_path)

    sys.exit(0)


def open_bval_file(file_path, log):
    '''
    opens a bval file and returns a list of floats.
    
    Parameters
    ----------
    file_path : str
        The path to the file to be opened.
    
    Returns
    -------
    num_list : list
        A list of floats.
    
    Examples
    --------
    >>> open_bval_file("/home/user/bval_file.bvals")
    [0.5, 0.3, 0.2]
    '''
    with open(file_path) as f:
        lines = f.readlines()
    if len(lines) < 1:
        log.add_msg(f"error: input meta file is either empty or can not be opened ({file_path}", is_error_msg=True)
        sys.exit(-1)
    if len(lines) > 1:
        log.add_msg(f"warning: input meta file is not of the proper form ({file_path}", is_error_msg=True)
    line = lines[0]
    if line[-1] == '\n':
        line = line[:-1]
    str_list = line.split('\t')
    num_list = [float(s) for s in str_list]

    return num_list


def open_bvec_file(file_path, log):
    '''
    takes a file path to a bvec file and returns a list of tuples
    containing the x, y, and z components of the bvecs.

    Parameters
    ----------
    file_path : str
        The path to the bvec file.

    Returns
    -------
    vect_list : list of tuples
        A list of tuples containing the x, y, and z components of the bvecs.

    Examples
    --------
    >>> open_bvec_file('/path/to/bvec_file.bvecs')
    [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    '''
    with open(file_path) as f:
        lines = f.readlines()
    if len(lines) < 3:
        log.add_msg(f"error: input meta file is either empty or not of the proper form ({file_path}", is_error_msg=True)
        sys.exit(-1)
    if len(lines) > 3:
        log.add_msg(f"warning: input meta file is not of the proper form ({file_path}", is_error_msg=True)

    if lines[0][-1] == '\n':
        lines[0] = lines[0][:-1]
    if lines[1][-1] == '\n':
        lines[1] = lines[1][:-1]
    if lines[2][-1] == '\n':
        lines[2] = lines[2][:-1]

    x_str = lines[0].split('\t')
    y_str = lines[1].split('\t')
    z_str = lines[2].split('\t')

    x = [float(s) for s in x_str]
    y = [float(s) for s in y_str]
    z = [float(s) for s in z_str]

    if (len(x) != len(y)) or (len(x) != len(z)) or (len(x) == 0):
        log.add_msg(f"error: input meta file is not of the proper form ({file_path}", is_error_msg=True)
        sys.exit(-1)

    vect_list = [(x[i], y[i], z[i]) for i in range(len(x))]

    return vect_list


if __name__== "__main__":
    main()
