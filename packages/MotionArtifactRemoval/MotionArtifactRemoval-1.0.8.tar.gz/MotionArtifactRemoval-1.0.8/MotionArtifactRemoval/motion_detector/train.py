import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline

class MotionFrameDetector:
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
        # over = SMOTE(sampling_strategy=0.5)
        over = ADASYN(sampling_strategy=0.5)
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
        fig = plt.figure(dpi=75, figsize=(12,12))

        k = 1
        for classifier_name, classifier_confusion_matrix in zip(self.classifier_names, self.classifier_confusion_matrices):
            plt.subplot(4,2,k)
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