import os
import sys
import numpy as np
import pandas as pd
import tifffile as tiff
from skimage.restoration import estimate_sigma
from collections import Counter
import matplotlib.pyplot as plt

from ..mmar import process_slice



def feature_extractor(image, mask):
    # individual image feature extractor
    features = [
        np.mean(image), 
        np.std(image), 

        np.mean(image[mask]), 
        np.std(image[mask]), 
        np.mean(image[mask]) / np.std(image[mask]),
        
        np.mean(image[mask==False]), 
        np.std(image[mask==False]), 
        np.mean(image[mask==False]) / np.std(image[mask==False]),
        
        estimate_sigma(image),
        
        psnr(image, image*mask),
        psnr(image, image*(1-mask))
        ]
    return features

def extract_features_for_all(parent_folder, mouse_list):

    features = {}
    for mouse in mouse_list:
        print(mouse)
        tif_file = os.path.join(parent_folder, mouse, 'dti_large_0.tif')
        if not os.path.isfile(tif_file):
            features[mouse]=[]
            continue

        img = tiff.imread(tif_file)[1:,:,:,:]
        nframes, nslices, nx, ny = img.shape
        nf_static = 11 # number of static features
        nf_dynamic = 7 # number of dynamic features -- has some information beyond 2D image
        features[mouse] = np.empty((nframes, nslices, nf_static+nf_dynamic))
        for i in range(nframes):
            for j in range(nslices):
                mask = process_slice.create_mask(img[i,j,:,:], fg=False)[0]
                features[mouse][i,j,:nf_static] = feature_extractor(img[i,j,:,:], mask)
            # add general slice feature to each individual frame // based on Median Absloute Deviation

        for j in range(nslices):
            allframes_data_median = np.median(features[mouse][:,j,0])
            allframes_fg_data_median = np.median(features[mouse][:,j,2])
            allframes_bg_data_median = np.median(features[mouse][:,j,4])
            allframes_MAD = np.median([np.abs(features[mouse][:,j,0] - allframes_data_median)])
            allframes_fg_MAD = np.median([np.abs(features[mouse][:,j,2] - allframes_fg_data_median)])
            allframes_bg_MAD = np.median([np.abs(features[mouse][:,j,4] - allframes_bg_data_median)])
            for i in range(nframes):
                features[mouse][i,j,nf_static] = allframes_fg_data_median
                features[mouse][i,j,nf_static+1] = allframes_fg_MAD
                features[mouse][i,j,nf_static+2] = allframes_bg_data_median
                features[mouse][i,j,nf_static+3] = allframes_bg_MAD
                features[mouse][i,j,nf_static+4] = allframes_MAD
                features[mouse][i,j,nf_static+5] = allframes_data_median
                features[mouse][i,j,nf_static+6] = j    

            
    return features

def psnr(img1, img2):
    '''
    Peak Signal to Noise Ratio
    '''
    mse = np.mean((img1 - img2) ** 2)
    return 20*np.log10(np.max(img1) / np.sqrt(mse))

def find_excel_file(folder_path):
    file_list = os.listdir(folder_path)
    excel_file_list = []
    for file in file_list:
        if file.endswith(".xlsx") and not file.startswith("~"):
            excel_file_list.append(file)
    return excel_file_list

def get_rejected_frames(parent_folder, mouse_list):

    rejected = {}
    for mouse in mouse_list:
        rejected_frames_file = find_excel_file(os.path.join(parent_folder,mouse))
        assert len(rejected_frames_file)==1, f"more than one excel file in {mouse}"
        df = pd.read_excel(os.path.join(parent_folder,mouse,rejected_frames_file[0]))
        rejected[mouse] = [[]]*17
        for i, val in enumerate(df[df.columns[0]]):
            if isinstance(val, int): 
                if isinstance(df.iloc[i,1], str):
                    rejected[mouse][val-1]=[int(i)-2 for i in df.iloc[i,1].split(',') if len(i)>0]
                elif isinstance(df.iloc[i,1], int):
                    rejected[mouse][val-1]=df.iloc[i,1]-2
    return rejected


def set_to_one(A, B):
    for i in range(len(A)):
        if A[i] != []:
            if isinstance(A[i], int):
                B[A[i]][i] = 1
                continue
            for j in A[i]:
                B[j][i] = 1
    return B

def plot_features(X, Y, n):
    fig = plt.figure(dpi=75, figsize=(8,8))

    k = 1

    for j in range(X.shape[1]):
        plt.subplot(5,5,k)
        counter = Counter(Y)
        for label, _ in counter.items():
            row_ix = np.where(Y == label)[0]
            plt.scatter(X[row_ix, n], X[row_ix, j], label=str(label))
        k+=1

    plt.legend()
    plt.show()