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
from sklearn.externals import joblib

import fasttext


# Import our custom scripts
sys.path.append('libs/')
import textfeatures
import fileio
import classification

fasttext_model_train_file = 'data/train/annotated_fb_messages.txt'
fasttext_textfeature_file = '../fastText/data/wiki.fi.bin'
predictor_model_file = 'data/models/fasttext_rf.pkl'

def main(args):

    if os.path.exists(os.path.dirname(predictor_model_file)) == False:
        os.makedirs(os.path.dirname(predictor_model_file))

    # Load training data
    # TODO: This data should come from real database
    print('Loading training data')
    y, messages, classes = fileio.read_fasttext_train_file(fasttext_model_train_file)
    y = np.array(y)

    #TODO: We need to have BoW Features here too..
    # Load FastText textfeatures
    print('Loading text feature extractor')
    model = fasttext.load_model(fasttext_textfeature_file)


    # Extract text features from training data
    print('Extracting text features from training data')
    x = textfeatures.fasttext_bag_of_means(messages, model)

    # Train the model
    # TODO: It would make sense to define training as a pipeline so that all the
    # parameters could be given in
    print('Training a new model..')
    clf = RF().fit(x, y)

    # Save the model
    #TODO: The name of the file should be also depend on the method
    print('Storing the result file in %s' % predictor_model_file)
    joblib.dump(clf, 'data/models/fasttext_rf.pkl')

if __name__ == "__main__":
    main(sys.argv)
