# %%
# from torch.utils.data import Dataset
# import torchvision.transforms.functional as F
import numpy as np
import SimpleITK as sitk
from utils import cvt1to3channels, normalize_image
import random
from PIL import Image
# from torchvision import transforms
import os
from random import seed, shuffle

def load_data(data_path, num_train_sample, modality=None):

    train_path = data_path + 'training/' 
    mask_path = data_path + 'masks/' 
    train_list = sorted(os.listdir(train_path))

    mouse_name = np.unique([f[:24] for f in train_list if f[:6]=='CK_DIF'])
    seed(10)
    shuffle(mouse_name)
    mouse_train = mouse_name[:num_train_sample]
    mouse_val   = mouse_name[num_train_sample:]

    train_list = [i for i in train_list if i[-2:]=='gz']

    src_train, msk_train, fnames_train = [], [], []
    src_val, msk_val, fnames_val = [], [], []

    # Read indiviual "nii.gz" files
    for f in train_list:
        if modality and modality not in f:
                continue
        # Read the entire volume
        training_arr = sitk.GetArrayFromImage(sitk.ReadImage(train_path + f))
        
        # 'noddi' images have 4 dimentions
        if len(training_arr.shape)==4:
            training_arr = training_arr[0,:,:,:]
        
        mask_arr = sitk.GetArrayFromImage(sitk.ReadImage(mask_path + f.replace('data','mask')))

        for image_idx in range(training_arr.shape[0]):
            # Preprocess and transform training data
            input_image_original = training_arr[image_idx, :,:]
            input_image_original = normalize_image(input_image_original)

            # Transform expert mask
            input_mask_original = mask_arr[image_idx, :,:]
            input_mask_original = normalize_image(input_mask_original)
            if f[:24] in mouse_train:
                src_train.append(np.uint8(input_image_original))
                msk_train.append(np.uint8(input_mask_original))
                fnames_train.append((f, image_idx))
            elif f[:24] in mouse_val:
                src_val.append(np.uint8(input_image_original))
                msk_val.append(np.uint8(input_mask_original))
                fnames_val.append((f, image_idx))
            else:
                print(f'{f} is not in train or validation mouse list!')
            
    return src_train, msk_train, src_val, msk_val, fnames_train, fnames_val
