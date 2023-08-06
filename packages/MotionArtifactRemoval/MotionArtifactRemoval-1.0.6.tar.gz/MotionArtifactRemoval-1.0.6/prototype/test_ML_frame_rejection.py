#%%
import os
import sys
import numpy as np
import pandas as pd
import tifffile as tiff
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
from skimage.restoration import estimate_sigma
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mmar'))
import process_slice

class Classifier:
    def __init__(self, X, Y, train_balanced=False):
        self.X = X
        self.Y = Y
        
        self.train_balanced = train_balanced

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=23)
        
        sc = StandardScaler()
        self.X_train = sc.fit_transform(self.X_train)
        self.X_test = sc.transform(self.X_test)

        self.classifiers = [
            LogisticRegression(), 
            SVC(kernel='linear',probability=True), 
            SVC(probability=True), 
            RandomForestClassifier(),
            AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                         algorithm="SAMME",
                         n_estimators=200),
            GradientBoostingClassifier(n_estimators=100, learning_rate=.1, max_depth=2),
            GaussianNB()
            ]
        
        self.classifier_names = [
            'Logistic Regression', 
            'SVM with linear kernel', 
            'SVM', 
            'Random Forest', 
            'AdaBoosted decision tree', 
            'Gradient Boosted Decision Tree',
            'Gaussian Naive Bayes',
            ]
        
        self.classifier_accuracies = []
        self.classifier_predictions = []
        self.classifier_probabilities = []
        self.classifier_confusion_matrices = []
        self.classifier_classification_reports = []
        self.classifier_roc_auc_scores = []
        self.classifier_roc_curves = []
        self.classifier_balanced_accuracy = []

    def train(self):
        if self.train_balanced:
            X, y = self.balance_data(self.X_train, self.Y_train)
        else:
            X, y = self.X_train, self.Y_train
        for classifier, classifier_name in zip(self.classifiers, self.classifier_names):
            classifier.fit(X, y)
            self.classifier_accuracies.append(classifier.score(self.X_test, self.Y_test))
            self.classifier_predictions.append(classifier.predict(self.X_test))
            self.classifier_probabilities.append(classifier.predict_proba(self.X_test))
            self.classifier_confusion_matrices.append(confusion_matrix(self.Y_test, self.classifier_predictions[-1]))
            self.classifier_classification_reports.append(classification_report(self.Y_test, self.classifier_predictions[-1]))
            self.classifier_roc_auc_scores.append(roc_auc_score(self.Y_test, self.classifier_probabilities[-1][:, 1]))
            self.classifier_roc_curves.append(roc_curve(self.Y_test, self.classifier_probabilities[-1][:, 1]))
            self.classifier_balanced_accuracy.append(balanced_accuracy_score(self.Y_test, self.classifier_predictions[-1]))
    
    def balance_data(self, X, y):
        '''
        balance the minority class 
        ref: https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/
        '''
        over = SMOTE(sampling_strategy=0.5)
        under = RandomUnderSampler(sampling_strategy=0.5)
        steps = [('o', over), ('u', under)]
        pipeline = Pipeline(steps=steps)
        X, y =pipeline.fit_resample(X, y)
        return X, y

    def print_results(self):
        for classifier_name, classifier_accuracy, classifier_balanced_accuracy, classifier_roc_auc_score in zip(self.classifier_names, self.classifier_accuracies, self.classifier_balanced_accuracy, self.classifier_roc_auc_scores):
            print('Accuracy of {}: {:.2f}%'.format(classifier_name, classifier_accuracy*100))
            print('Balanced Accuracy of {}: {:.2f}%'.format(classifier_name, classifier_balanced_accuracy*100))
            print('ROC AUC score of {}: {:.2f}%'.format(classifier_name, classifier_roc_auc_score*100))
            print('\n')

    def plot_confusion_matrices(self):
        fig = plt.figure(dpi=150, figsize=(20,20))

        k = 1
        for classifier_name, classifier_confusion_matrix in zip(self.classifier_names, self.classifier_confusion_matrices):
            plt.subplot(2,5,k)
            plt.imshow(classifier_confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
            plt.title('Confusion matrix for {}'.format(classifier_name))
            # plt.colorbar()
            tick_marks = np.arange(2)
            plt.xticks(tick_marks, ['0', '1'], rotation=45)
            plt.yticks(tick_marks, ['0', '1'])
            # plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            k+=1
        plt.show()

    def plot_roc_curves(self):
        plt.figure()
        for classifier_name, classifier_roc_curve in zip(self.classifier_names, self.classifier_roc_curves):
            plt.plot(classifier_roc_curve[0], classifier_roc_curve[1], label=classifier_name)
        plt.plot([0, 1], [0, 1], 'k--', label='')
        plt.axis([0, 1, 0, 1])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curves')
        plt.legend()
        plt.show()

    def plot_roc_auc_scores(self):
        plt.figure()
        plt.bar(range(len(self.classifier_roc_auc_scores)), self.classifier_roc_auc_scores, align='center')
        plt.xticks(range(len(self.classifier_roc_auc_scores)), self.classifier_names, rotation=45, ha='right')
        plt.title('ROC AUC score')
        plt.ylim((0.75, 1))
        plt.show()

    def plot_balanced_scores(self):
        plt.figure()
        plt.bar(range(len(self.classifier_balanced_accuracy)), self.classifier_balanced_accuracy, align='center')
        plt.xticks(range(len(self.classifier_balanced_accuracy)), self.classifier_names, rotation=45, ha='right')
        plt.title('Balanced Accuracy')
        plt.ylim((0.5, 1))
        plt.show()

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

parent_folder = '/Users/ghanba/Documents/ssif_data_jax/'
mouse_list = [f for f in os.listdir(parent_folder) if not f.startswith('.')]
mouse_list.sort()

mouse_list = mouse_list[:10]

rejected = get_rejected_frames(parent_folder, mouse_list)

features = extract_features_for_all(parent_folder, mouse_list)

X_all = []
Y_all = []
for mouse in mouse_list:
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


#%% scatter plot of the dataset
from collections import Counter
def plot_features(X, Y, n):
    fig = plt.figure(dpi=150, figsize=(20,20))

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
plot_features(X, Y, 11)
#%%

#%%
model = Classifier(X, Y, train_balanced=True)
model.train()
model.print_results()
model.plot_confusion_matrices()
model.plot_roc_curves()
model.plot_roc_auc_scores()
model.plot_balanced_scores()

