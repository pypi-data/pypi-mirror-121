#%%
import os
import numpy as np
import random
from .train import MotionFrameDetector
from .utils import *

def evaluate(n):
    parent_folder = '/Users/ghanba/Documents/ssif_data_jax/'
    mouse_list = [f for f in os.listdir(parent_folder) if not f.startswith('.')]
    mouse_list.sort()

    mouse_list = random.sample(mouse_list[:95], n)

    rejected = get_rejected_frames(parent_folder, mouse_list)

    features = extract_features_for_all(parent_folder, mouse_list)

    X_all = []
    Y_all = []
    for mouse in mouse_list:
        print(mouse)
        X = features[mouse]
        if isinstance(X_all, list):
            X_all = np.expand_dims(X, axis=0)
        else:
            X_all = np.concatenate((X_all, np.expand_dims(X, axis=0)), axis=0)
        
        Y = set_to_one(rejected[mouse], np.zeros((X.shape[0], X.shape[1])))
        if isinstance(Y_all, list):
            Y_all = np.expand_dims(Y, axis=0)
        else:
            Y_all = np.concatenate((Y_all, np.expand_dims(Y, axis=0)), axis=0)
        
    X_all = X_all[:,:,:,:]
    X = X_all.reshape(-1, X_all.shape[-1])
    Y = Y_all.reshape(-1)


    # scatter plot of the dataset
    plot_features(X, Y, 11)

    model = MotionFrameDetector(X, Y, train_balanced=True)
    model.train()
    model.print_results()
    model.plot_confusion_matrices()
    model.plot_roc_curves()
    model.plot_roc_auc_scores()
    model.plot_balanced_scores()
    return model

if __name__ == '__main__':
    evaluate(5)

# %%
