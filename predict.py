#!/usr/local/bin/python3
'''

This script predicts/detects hate speech for new messages

'''

import sys
import argparse
import os
import glob

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
    parser.add_argument('--inputdir', help='Input directory', required=True)
    #parser.add_argument('--output', help='Output', default='predictions.csv')
    parser.add_argument('--outdir', help='Directory to store data', default='data/output', required=True)
    parser.add_argument('--featurename', help='Feature extraction name', required=True)
    parser.add_argument('--featurefile', help='Feature extraction file', required=True)
    parser.add_argument('--predictor', help='Predictor file', required=True)

    args = parser.parse_args(argv[1:])

    print('Inputs:')
    print(args)

    # Load FastText textfeatures
    print('Loading text feature extractor')
    feature_extractor = textfeatures.FeatureExtractor(method=args.featurename,
                                                      filename=args.featurefile)

    # Load the preditor model
    clf = joblib.load(args.predictor)

    filenames = glob.glob(os.path.join(args.inputdir, '*.csv'))
    for filename in filenames:
        # Load new messages
        df = pd.read_csv(filename) #args.input)
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
        outputfile = os.path.join(args.outdir, os.path.basename(filename))
        if (len(os.path.dirname(outputfile)) > 0) and (not os.path.exists(os.path.dirname(outputfile))):
            os.makedirs(os.path.dirname(outputfile))
        print('Storing results to %s' % outputfile)
        df.to_csv(outputfile)

if __name__ == '__main__':
    main(sys.argv)
