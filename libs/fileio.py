import sys
import glob
import os

import pandas as pd
import numpy as np

sys.path.append('confs/')
sys.path.append('libs/')


def dump_tweets_to_file(filename='data/tweets.txt'):
    import database

    db = database.HateBase()
    db.get_tweets()
    tweets = db.get_tweets()
    with open(filename, 'w') as f:
        for tweet in tweets:
            f.write(tweet.replace('\n',' ') + '\n')

def read_fasttext_train_file(filename):
    classes = ['__label__OK', '__label__vihapuhetta']
    class_ids = []
    msgs = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            tokens = line.split(' ')
            class_name = tokens[0]
            msg = ' '.join(tokens[1:])
            # define class_id
            if classes.count(class_name) == 0:
                classes.append(class_name)
            class_ids.append(classes.index(class_name))
            msgs.append(msg)
    return class_ids, msgs, classes

def read_annotated_files(dirname):

    messages = []
    labels = np.zeros(0)

    filenames = glob.glob(os.path.join(dirname, '*.xls*'))

    for filename in filenames:
        print('Reading %s' % filename, end='. ', flush=True)

        df = pd.read_excel(filename)
        print("Found %d new samples" % df[df.LABEL.notnull()].shape[0])
        labels = np.hstack((labels, np.array(df[df.LABEL.notnull()].LABEL.tolist(),
                           dtype=int)))
        messages += df[df.LABEL.notnull()].text.tolist()


    return messages, labels
