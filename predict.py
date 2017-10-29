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
import texttools # For hatewords stemming
import fileio
import classification

class HateWordDetector:

    def __init__(self, filename):
        self.filename = filename
        self.hatewords = []
        self.stemmed_hatewords = []
        self.stemming2original = []

        self.load_hatewords(filename)

    def load_hatewords(self, filename):

        self.hatewords = open(filename, 'r').read().splitlines()
        self.stemmed_hatewords, self.stemming2original = texttools.stemming_messages_snowball(self.hatewords)

    def detect_hatewords(self, message):

        stemmed_message, stemming2original = texttools.stemming_message_snowball(message, self.stemming2original.copy())
        n_hate_words = 0
        hate_words_in_message = []
        for word in stemmed_message.split():
            if word in self.stemmed_hatewords:
                n_hate_words += 1
                hate_words_in_message.append(stemming2original[word])

        return n_hate_words, hate_words_in_message


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

    # Load HateWords counter
    hwd = HateWordDetector('data/vihasanat.txt')

    filenames = glob.glob(os.path.join(args.inputdir, '*.json'))
    for filename in filenames:

        # Skip if messages have been predicted already
        outputfile = os.path.join(args.outdir, os.path.basename(filename).replace('json','csv'))
        if os.path.exists(outputfile):
            continue

        # Load new messages
        df = pd.read_json(filename) #args.input)
        messages = df.text.tolist()

        # Extract features
        print('Extracting text features from new data')
        x = feature_extractor.extract(messages)

        # predict hate speech messages
        print('Predicting hate speech messages..')
        pred = clf.predict(x)
        score = clf.predict_proba(x)[:,1]

        # Compute the number of hatewords in each message
        n_hate_words = np.zeros(len(messages))
        for i, message in enumerate(messages):
            n_hate_words[i], _ = hwd.detect_hatewords(message)

        # Update dataframe
        df['n_hate_words'] = n_hate_words
        df['predicted_label'] = pred
        df['prediced_score'] = score

        # Store result
        if (len(os.path.dirname(outputfile)) > 0) and (not os.path.exists(os.path.dirname(outputfile))):
            os.makedirs(os.path.dirname(outputfile))
        print('Storing results to %s' % outputfile)
        df.to_csv(outputfile)

if __name__ == '__main__':
    main(sys.argv)
