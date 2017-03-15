#!/usr/local/bin/python3
'''

Train Feature extractor

'''

import sys
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

import fasttext

sys.path.append('libs/')
import fileio
import textfeatures
import classification

y, messages, classes = fileio.read_fasttext_train_file('data/train/annotated_fb_messages.txt')

bow = TfidfVectorizer().fit(messages)

joblib.dump(bow, 'data/models/feature_extractor_bow.pkl')
