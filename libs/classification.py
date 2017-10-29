import numpy as np

from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import fasttext

def run_kfold_test(clf, x, y, k=10):
    '''
        Runs k-Fold test for model benchmarking.
        o Inputs:
            - clf is a classifier to be trained, tested and evaluated
            - x is input features
            - y is target labels
            - k defines the number of test-splits
    '''
    kf = KFold(k)

    results = []

    for train_idx, test_idx in kf.split(x, y):

        # Train and test split
        x_train = x[train_idx]
        x_test = x[test_idx]
        y_train = y[train_idx]
        y_test = y[test_idx]

        # Training
        clf.fit(x_train, y_train)

        ## Evaluation
        # Train-set
        pred = clf.predict(x_train)
        train_f1 = f1_score(y_train, pred)
        train_acc = accuracy_score(y_train, pred)
        cm = confusion_matrix(y_train, pred)
        train_trp = cm[1, 1] / np.sum(cm[1, :])

        # Test-set
        pred = clf.predict(x_test)
        test_f1 = f1_score(y_test, pred)
        test_acc = accuracy_score(y_test, pred)
        cm = confusion_matrix(y_test, pred)
        test_trp = cm[1, 1] / np.sum(cm[1, :])

        print(train_acc, train_f1, train_trp, test_acc, test_f1, test_trp, sep='\t')
        results.append([train_acc, train_f1, train_trp, test_acc, test_f1, test_trp, clf])

    result = np.array(results)
    return results

class skfasttext:

    def __init__(self, train_file = '/tmp/fasttext_train.txt'):
        'Creates a new SciKit-Learn style wrapped FastText object'
        self.train_file = train_file
        self.model = None


    def fit(self, x, y):
        '''
        Traines a supervised classifier.
        o Inputs:
            - x is a list of text documents
            - y is a list or array with numerical labels (0 OK and 1 hatespeech)
        '''

        with open(self.train_file, 'w') as f:
            for xi, yi in zip(x, y):
                if yi == 0:
                    f.write('__label__OK ')
                else:
                    f.write('__label__vihapuhetta ')
                f.write(xi.replace('\n', ' ') + '\n')
        self.model = fasttext.supervised(self.train_file, 'model', label_prefix='__label__')

    def predict(self, x):
        '''
        Predicts/classifies given samples
         o Input:
            - x is a list of text documents
        '''

        predictions = self.model.predict(x)

        pred = np.zeros(len(predictions))

        for i in range(0, len(predictions)):
            pred[i] = self.model.labels.index(predictions[i][0])

        return pred
