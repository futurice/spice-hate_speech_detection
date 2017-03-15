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

import fasttext


# Import our custom scripts
sys.path.append('libs/')
import textfeatures
import fileio
import classification

#fasttext_model_train_file = 'data/train/annotated_fb_messages.txt'
#fasttext_textfeature_file = '../fastText/data/wiki.fi.bin'
#predictor_model_file = 'data/models/fasttext_rf.pkl'

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input')
    parser.add_argument('--output', help='Output', default='predictions.csv')
    parser.add_argument('feature', help='Feature extraction file')
    parser.add_argument('feature_method', help='Feature extraction method', default='fasttext')
    parser.add_argument('classifier', help='Predictor file')

    args = parser.parse_args(argv)

    print('Inputs:')
    print(args)

    # Load training data
    # TODO: This data should come from real database
    print('Loading training data')
    y, messages, classes = fileio.read_fasttext_train_file(args.input)
    y = np.array(y)

    #TODO: We need to have BoW Features here too..
    # Load FastText textfeatures
    print('Loading text feature extractor')
    feature_extractor = textfeatures.FeatureExtractor(method=args.feature_method,
                                                      filename=args.feature)


    # Extract text features from training data
    print('Extracting text features from training data')
    x = feature_extractor.extract(messages)

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
    predictor_model_file = os.path.join('data', 'models', args.feature_method +
                                        '_' + args.classifier + '.pkl')
    if os.path.exists(os.path.dirname(predictor_model_file)) == False:
        os.makedirs(os.path.dirname(predictor_model_file))
    print('Storing the result file in %s' % predictor_model_file)
    joblib.dump(clf, predictor_model_file)

if __name__ == "__main__":
    main(sys.argv[1:])
