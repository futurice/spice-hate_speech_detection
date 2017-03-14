import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.svm import SVC
import fasttext

sys.path.append('libs/')
import fileio
import textfeatures
import classification

y, messages, classes = fileio.read_fasttext_train_file('data/train/annotated_fb_messages.txt')
y = np.array(y)

x = textfeatures.bag_of_words(messages, model=None, weighting='tfidf')

import classification

print("Random Forest:")
clf = RF(n_estimators = 10)
results = classification.run_kfold_test(clf, x, y)
print(np.mean(results, axis=0), sep='\t')

print("SVM:")
clf = SVC(kernel='linear')
results = classification.run_kfold_test(clf, x, y)
print(np.mean(results, axis=0), sep='\t')
