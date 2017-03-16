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

## Usage:
### Collect new data
usage:

`collector.py [-h] [--user USER] [--password PASSWORD]
                    [--hostname HOSTNAME] [--outdir OUTDIR]
                    [--startdate STARTDATE] [--enddate ENDDATE]

optional arguments:
  -h, --help            show this help message and exit
  --user USER           Username
  --password PASSWORD   Password
  --hostname HOSTNAME   Hostname
  --outdir OUTDIR       Directory to store data
  --startdate STARTDATE
                        Startdate as YYYY-MM-DD
  --enddate ENDDATE     Enddate as YYYY-MM-DD`

Example:

`./collector.py --startdate 2017-03-01 --enddate 2017-03-15`

### Train predictor

Example:

`./predict.py --inputdir data/incoming --outdir data/output/ --featurename bow --featurefile data/models/feature_extractor_bow.pkl --predictor data/models/fasttext_svm.pkl`

### Predict hate speech

Example:

`./predict.py --inputdir data/incoming --outdir data/output/ --featurename bow --featurefile data/models/feature_extractor_bow.pkl --predictor data/models/bow_svm.pkl`

### Sync data
Example:

`./sync.py --inputdir data/output/`

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
