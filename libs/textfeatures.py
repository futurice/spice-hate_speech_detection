import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import texttools

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
