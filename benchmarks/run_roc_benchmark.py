'''
This script performs benchmark for different approaches and plots ROC curve
'''

import sys
import numpy as np

import pylab

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.svm import SVC

import fasttext

sys.path.append('libs/')
import textfeatures
import fileio
import classification

pylab.ion()
pylab.figure()

y, messages, classes = fileio.read_fasttext_train_file('data/train/annotated_fb_messages.txt')
y = np.array(y)

#
# FastText features
#
model = fasttext.load_model('data/tweets_skipgram.bin')
x = textfeatures.fasttext_bag_of_means(messages, model)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

## RF
# Train, predict and evaluate
clf = RF().fit(x_train, y_train)
score = clf.predict_proba(x_test)
fpr, tpr, _ = roc_curve(y_test==1, score[:,1])
# Plot
pylab.plot(fpr, tpr)

## SVC
# Train, predict and evaluate
clf = SVC(probability=True).fit(x_train, y_train)
score = clf.predict_proba(x_test)
fpr, tpr, _ = roc_curve(y_test==1, score[:,1])
# Plot
pylab.plot(fpr, tpr)

#
# BOW features
#
x = textfeatures.bag_of_words(messages, model=None, weighting='tfidf')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

## RF
# Train, predict and evaluate
clf = RF().fit(x_train, y_train)
score = clf.predict_proba(x_test)
fpr, tpr, _ = roc_curve(y_test==1, score[:,1])
# Plot
pylab.plot(fpr, tpr)

## SVC
# Train, predict and evaluate
clf = SVC(probability=True).fit(x_train, y_train)
score = clf.predict_proba(x_test)
fpr, tpr, _ = roc_curve(y_test==1, score[:,1])
# Plot
pylab.plot(fpr, tpr)

pylab.legend(('FT + RF', 'FT + SVM', 'BOW + RF', 'BOW + SVM'))
pylab.xlabel('FPR')
pylab.ylabel('TPR'
pylab.waitforbuttonpress()
