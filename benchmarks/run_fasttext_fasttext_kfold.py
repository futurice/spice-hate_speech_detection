import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.svm import SVC
import fasttext

sys.path.append('libs/')
import textfeatures
import fileio
import classification

y, x, classes = fileio.read_fasttext_train_file('data/train/annotated_fb_messages.txt')
y = np.array(y)

print("fasttext:")
clf = classification.skfasttext()
results = classification.run_kfold_test(clf, x, y)
print(np.mean(results, axis=0), sep='\t')
