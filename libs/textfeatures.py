import os

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

import texttools
import fasttext

def fasttext_bag_of_means(messages, model):

    x = np.zeros((len(messages), model.dim))

    for i, message in enumerate(messages):
        for word in message.split():
            x[i, :] += model[word]

    return x

def bag_of_words(messages, model=None, weighting=''):

    # TODO: Add stemmming or baseform here
    messages, stemmings2baseform =  texttools.stemming_messages_snowball(messages)

    # Create new model for extrating text features if None is given
    if model is None:
        if weighting == 'tfidf':
            model = TfidfVectorizer()
        else:
            model = CountVectorizer()
        model.fit(messages)

    # Extract features
    x = model.transform(messages)

    return x

class FeatureExtractor:
    def __init__(self, method='fasttext', filename=''):

        self.method = method
        self.filename = filename
        self.model = None

        # If a filename is given, try to load the model
        if os.path.exists(self.filename):
            self.load_model()

    def load_model(self, filename=''):

        # Define path to the feature extractor model filename
        if (len(filename) > 0) and os.path.exists(filename):
            self.filename = filename
        if not os.path.exists(self.filename):
            print('Feature file %s does not exist' % self.filename)
            return -1

        print('Loading model %s' % self.filename)
        if self.method == 'fasttext':
            self.model = fasttext.load_model(self.filename)
        elif self.method == 'bow':
            self.model = joblib.load(self.filename)

    def extract(self, documents):

        if self.method == 'fasttext':
            x = fasttext_bag_of_means(documents, self.model)
        elif self.method == 'bow':
            x =  bag_of_words(documents, self.model)

        return x
