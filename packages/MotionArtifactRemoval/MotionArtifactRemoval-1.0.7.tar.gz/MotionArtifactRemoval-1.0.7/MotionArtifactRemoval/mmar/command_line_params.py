# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime

from version import version

_desc = "mmar - (MRI motion artifact removal) Identify and remove frames showing motion artifacts"

_epilog = ""
_epilog += '-------------------------------------------------------------------------------------------------------' + os.linesep
_epilog += 'The <input_scan> is an image file (tif or nii.gz) containing a list of multi-frame slice images' + os.linesep
_epilog += 'The "bvecs" and "bvals" files contain the corresponding diffusion metadata.  Both are tab-separated files.' + os.linesep
_epilog += 'The bvals file is a single record, while the bvecs file is three records for the x, y, z components separated.' + os.linesep
_epilog += 'Intensity values in the bvals file that are less than "bvals_threshold" are assumed to be non-diffusion' + os.linesep
_epilog += 'frames, indicating the start of a new scan.' + os.linesep
_epilog +=  os.linesep
_epilog += 'When run successfully, the output directory will be populated with the following:' + os.linesep
_epilog += '    <output_dir>' + os.linesep
_epilog += '        <log.txt>' + os.linesep
_epilog += '        excluded_frames.csv' + os.linesep
_epilog += '        <scan_directory>' + os.linesep
_epilog += '            <slice_directory>' + os.linesep
_epilog += '                image.nii.gz' + os.linesep
_epilog += '                image.tif' + os.linesep
_epilog += '                mask.tif' + os.linesep
_epilog += '                meta.bvals' + os.linesep
_epilog += '                meta.bvecs' + os.linesep
_epilog += '                profile.jpg' + os.linesep
_epilog += ' ' + os.linesep
_epilog += 'The file "excluded_frames.csv" contains comma-separated values, with one line per slice, listing' + os.linesep
_epilog += 'the frames that were excluded from the original image.  In each record, the first two columns list the ' + os.linesep
_epilog += 'scan index and the slice index, followed by rejected frames.  NOTE: All indices are 0-based.' + os.linesep
_epilog += ' ' + os.linesep
_epilog += 'If the input image contains only one scan the the <scan> directory will be dropped, otherwise' + os.linesep
_epilog += 'the first and second scan directories will be named "small_shell", and "large_shell", and' + os.linesep
_epilog += 'subsequent directories, "scan_03", "scan_04"..., etc.' + os.linesep
_epilog += os.linesep
_epilog += 'Each slice directory contains:' + os.linesep
_epilog += '    image.nii.gz - multi-frame slice image with rejected frames removed' + os.linesep
_epilog += '    image.tif - same as above, in tif format' + os.linesep
_epilog += '    meta.bvals - copy of original bvals file with rejected frames removed' + os.linesep
_epilog += '    meta.bvecs - copy of original bvecs file with rejected frames removed' + os.linesep
_epilog += '    mask.tif - mask used to separate tissue area from background' + os.linesep
_epilog += '    profile.jpg - profile of average intensities in foreground and background across all original frames' + os.linesep
_epilog += '-------------------------------------------------------------------------------------------------------' + os.linesep
_epilog += os.linesep



class command_line_params:
    scan_file = ""
    input_dir = "./"
    output_dir = "./results/"
    bvals_file = ""
    bvecs_file = ""
    scan_path = ""
    bvals_path = ""
    bval_thresh = 10.0
    bvecs_path = ""
    rejected_frames_file = ""
    fg_thresh = 6.0
    bg_thresh = 3.5
    log_file = "log.txt"
    log_file_path = ""
    verbose = False



    def __init__(self):
        parser = argparse.ArgumentParser(description=_desc, formatter_class=RawTextHelpFormatter, epilog=_epilog)
        parser.add_argument("input_scan", help="multi-frame 3D scan")
        parser.add_argument('-i', metavar='input_dir', default=self.input_dir, help="directory containing input files. Default="+self.input_dir)
        parser.add_argument('-o', metavar='output_dir', default=self.output_dir, help="directory for results. Default="+self.output_dir)
        parser.add_argument('-bvecs', metavar='bvecs_file', default=self.bvecs_file, help="input bvecs file - When not specified the scan file base + '.bvecs' is used")
        parser.add_argument('-bvals', metavar='bvals_file', default=self.bvals_file, help="input bvals file - When not specified the scan file base + '.bvals' is used")
        parser.add_argument('-n', metavar='bvals_threshold', type=float, default=self.bval_thresh, help="non-diffusion bval threshold, to determine begining of scan (e.g. 10.0)")
        parser.add_argument('-r', metavar='rejected_frames', default=self.rejected_frames_file, help="When specified, overriding automatic detection")
        parser.add_argument('-fg', metavar='fg_thresh', type=float, default=self.fg_thresh, help="foreground threshold for MAD algorithm (e.g. 6.0)")
        parser.add_argument('-bg', metavar='bg_thresh', type=float, default=self.bg_thresh, help="background threshold for MAD algorithm (e.g. 3.5)")
        parser.add_argument('-log', metavar='log_file', type=str, default=self.log_file, help="log file to be created in the output directory")
        parser.add_argument('-v', dest='verbose', action='store_true', help="print messages to console")

        args = parser.parse_args()

        self.scan_file = args.input_scan
        self.input_dir = args.i
        self.output_dir = args.o
        self.bvecs_file = args.bvecs
        self.bvals_file = args.bvals
        self.bval_thresh = args.n
        self.rejected_frames_file = args.r
        self.fg_thresh = args.bg
        self.fg_thresh = args.fg
        self.log_file = args.log
        self.verbose = args.verbose
        return

    def check_parameters(self):
        i = self.scan_file.rfind('.nii')
        if i<= 0:
            i = self.scan_file.rfind('.tif')
        if i <= 0:
            print(f'error: input DTI scan must be either a "tif" or "nii" file: {self.scan_file}')
            sys.exit(-1)

        base_input_file = self.scan_file[:i]
        if base_input_file.endswith("_0"):
            base_input_file = base_input_file[:-2]
        if not self.bvecs_file:
            self.bvecs_file = base_input_file + ".bvecs"
        if not self.bvals_file:
            self.bvals_file = base_input_file + ".bvals"

        self.scan_path = os.path.join(self.input_dir, self.scan_file)
        self.bvals_path = os.path.join(self.input_dir, self.bvals_file)
        self.bvecs_path = os.path.join(self.input_dir, self.bvecs_file)
        self.log_file_path = os.path.join(self.output_dir, self.log_file)

        if not os.path.isfile(self.scan_path):
            print(f"\nerror: input image file does not exist ({self.scan_path})\n")
            sys.exit(-1)
        if not os.path.isfile(self.bvals_path):
            print(f"\nerror: input bvals file does not exist ({self.bvals_path})\n")
            sys.exit(-1)
        if not os.path.isfile(self.bvecs_path):
            print(f"\nerror: input bvecs file does not exist ({self.bvecs_path})\n")
            sys.exit(-1)

        return


    def params_message(self):
        cumulative_string = os.linesep
        cumulative_string += f"mmar version {version().str}{os.linesep}"
        cumulative_string += f"    date run: {datetime.today().strftime('%m/%d/%Y %H:%M')}{os.linesep}"
        cumulative_string += f"    scan = {self.scan_file}{os.linesep}"
        cumulative_string += f"    input_dir = {self.input_dir}{os.linesep}"
        cumulative_string += f"    output_dir = {self.output_dir}{os.linesep}"
        cumulative_string += f"    bvals_file = {self.bvals_file}{os.linesep}"
        cumulative_string += f"    bvecs_file = {self.bvecs_file}{os.linesep}"
        cumulative_string += f"    bvals_threshold = {self.bval_thresh}{os.linesep}"
        cumulative_string += f"    fg_thresh = {self.fg_thresh}{os.linesep}"
        cumulative_string += f"    bg_thresh = {self.bg_thresh}{os.linesep}"
        if self.rejected_frames_file:
            cumulative_string += f"    rejected_frames = {self.rejected_frames_file}{os.linesep}"
        return cumulative_string

