#  Automatic hate speech detection

## Setup
1. Install requirements
  - python3
  - python packages: pandas, sklearn, fasttext, sqlalchemy, ...
2. Configure collector
  - Edit hiit_collector.py.example and save it as hiit_collector.py
3. Configure PostgreSQL
  - Edit postgre_keys.py.example and save it as postgre_keys.py
4. Get the data
  - FastText model for Finnish trained by Facebook using Finnish Wikipedia:
  [Facebook's trained models](https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md)

## TODO
2. CNN on Embedding Matrix (c.f Willi)
3. Stemmings, stop words for BoW
4. Study SVM factors (with BoW)
5. Mezadona ? To Models
6. Plot TSNE manifolds for wikipedia model and twitter model
  - Highlight hatewords

# DONE:
1. Try Naive Bayes-classifier with BoW
  - Naive Bayes (Gaussian) did perform comparable to RF, but worse than SVM
  - With FastText it performed poorly
