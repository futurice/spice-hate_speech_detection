#!/usr/local/bin/python3
'''

This script trains a new (predictor) model and stores result in the datadir.
Text feature extraction needs to be separately.

'''

import sys
import argparse
import os

import numpy as np

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.model_selection import KFold

import fasttext


# Import our custom scripts
sys.path.append('libs/')
import textfeatures
import fileio
import classification

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input')
    parser.add_argument('--annotations', help='Directory for annotated files (extends training material)', default='')
    parser.add_argument('--outputdir', help='Output directory', required=True)
    parser.add_argument('--featurename', help='Feature extraction name', required=True)
    parser.add_argument('--featurefile', help='Feature extraction file', required=True)
    parser.add_argument('--classifier', help='Predictor file', required=True)
    parser.add_argument('--kfold', help='Number of splits in K-Fold', required=False)

    args = parser.parse_args(argv)

    print('Inputs:')
    print(args)

    # Load training data
    # TODO: This data should come from real database
    print('Loading training data')
    y, messages, classes = fileio.read_fasttext_train_file(args.input)
    y = np.array(y)

    print(len(messages), y.shape)
    if len(args.annotations) > 0:
        newmessages, labels = fileio.read_annotated_files(args.annotations)
        y = np.hstack((y, labels))
        messages += newmessages

    print(len(messages), len(y))

    if len(messages) != len(y):
        print("Data shape and annotations do not match!")
        return 0

    #TODO: We need to have BoW Features here too..
    # Load FastText textfeatures
    print('Loading text feature extractor')
    feature_extractor = textfeatures.FeatureExtractor(method=args.featurename,
                                                      filename=args.featurefile)


    # Extract text features from training data
    print('Extracting text features from training data')
    x = feature_extractor.extract(messages)

    print("Number of samples x features: %d x %d" % (x.shape[0], x.shape[1]))

    # Make sure that we have just two classes
    y = np.array(y > 0, dtype=int)

    # Select all the posite samples (hate speech) and some negative samples
    n_neg = np.sum(y)
    n_pos = np.sum(y == 0)

    print(n_neg, n_pos)

    # Train the model
    # TODO: It would make sense to define training as a pipeline so that all the
    # parameters could be given in
    print('Training a new model..')
    if args.classifier.upper() == 'RF':
        clf = RF().fit(x, y)
    elif args.classifier.upper() == 'SVM':
        clf = SVC(kernel='linear', probability=True).fit(x, y)

    # Save the model
    #TODO: The name of the file should be also depend on the method
    predictor_model_file = os.path.join(args.outputdir, args.featurename +
                                        '_' + args.classifier + '.pkl')
    if os.path.exists(os.path.dirname(predictor_model_file)) == False:
        os.makedirs(os.path.dirname(predictor_model_file))
    print('Storing the result file in %s' % predictor_model_file)
    joblib.dump(clf, predictor_model_file)

if __name__ == "__main__":
    main(sys.argv[1:])
