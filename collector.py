#!/usr/local/bin/python3
'''

This script predicts/detects hate speech for new messages

'''
import requests

import sys
from io import StringIO

import pandas as pd

sys.path.append('confs')
import hiit_collector

url = 'http://' + hiit_collector.username + ':' + hiit_collector.password + '@' + hiit_collector.hostname + '/tcat/api/querybin.php'
#TODO: Set startdate and enddate more nicely
r = requests.get(url,
                 params = {'resource': 'querybin/tweets',
                           'action' : 'tweet-export',
                           'startdate' : '2017-01-01 00:00:00 utc',
                           'enddate' : '2017-03-09 23:59:00 utc',
                           'bin' : 'Kuntavaalit' } )
# TODO: Store data to database
open('data/incoming.csv', 'w').write(r.text)
