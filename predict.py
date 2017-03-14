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

# TODO: These should be defined in confs or come from settings ..
fasttext_textfeature_file = 'data/train/annotated_fb_messages.txt'
predictor_model_file = 'data/models/fasttext_rf.pkl'
outfile = 'data/prediction_results.csv'

# Load FastText textfeatures
print('Loading text feature extractor')
text_model = fasttext.load_model('data/tweets_skipgram.bin')

# Load the preditor model
clf = joblib.load(predictor_model_file)

# Load new messages
df = pd.read_csv('data/incoming.csv')
messages = df.text.tolist()

# Extract features
print('Extracting text features from new data')
x = textfeatures.fasttext_bag_of_means(messages, text_model)

# predict hate speech messages
print('Predicting hate speech messages..')
pred =clf.predict(x)
score = clf.predict_proba(x)[:,1]

# Update dataframe
df['predicted_label'] = pred
df['prediced_score'] = score

# Store result
print('Storing results to %s' % outfile)
df.to_csv(outfile)
