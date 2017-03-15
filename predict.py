#!/usr/local/bin/python3
'''

This script predicts/detects hate speech for new messages

'''

import sys
import argparse
import os

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.externals import joblib

import fasttext

# Import our custom scripts
sys.path.append('libs/')
import textfeatures
import fileio
import classification

def main(argv):
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input')
    parser.add_argument('--output', help='Output', default='predictions.csv')
    parser.add_argument('feature', help='Feature extraction file')
    parser.add_argument('predictor', help='Predictor file')

    args = parser.parse_args(argv)

    print('Inputs:')
    print(args)

    # Load FastText textfeatures
    print('Loading text feature extractor')
    feature_extractor = textfeatures.FeatureExtractor(method='fasttext', filename=args.feature)

    # Load the preditor model
    clf = joblib.load(args.predictor)

    # Load new messages
    df = pd.read_csv(args.input)
    messages = df.text.tolist()

    # Extract features
    print('Extracting text features from new data')
    x = feature_extractor.extract(messages)

    # predict hate speech messages
    print('Predicting hate speech messages..')
    pred = clf.predict(x)
    score = clf.predict_proba(x)[:,1]

    # Update dataframe
    df['predicted_label'] = pred
    df['prediced_score'] = score

    # Store result
    if (len(os.path.dirname(args.output)) > 0) and (not os.path.exists(os.path.dirname(args.output))):
        os.makedirs(os.path.dirname(args.output))
    print('Storing results to %s' % args.output)
    df.to_csv(args.output)

if __name__ == '__main__':
    main(sys.argv[1:])
