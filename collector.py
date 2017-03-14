#!/usr/local/bin/python3
'''

This script predicts/detects hate speech for new messages

'''
import requests
import argparse
import sys
from io import StringIO
import datetime
import os

import pandas as pd

sys.path.append('confs')
import hiit_collector

def main(argv):
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--hostname', help='Hostname')
    parser.add_argument('--startdate', help='Startdate')
    parser.add_argument('--enddate', help='Startdate')

    args = parser.parse_args(argv)

    if args.user is None:
        args.user = hiit_collector.username
    if args.password is None:
        args.password = hiit_collector.password
    if args.hostname is None:
        args.hostname = hiit_collector.hostname
    if args.startdate is None:
        args.startdate = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00 utc')
    if args.enddate is None:
        args.enddate = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59 utc')

    # Get the data
    url = 'http://' + args.user + ':' + args.password + '@' + args.hostname + '/tcat/api/querybin.php'
    r = requests.get(url,
                     params = {'resource': 'querybin/tweets',
                               'action' : 'tweet-export',
                               'startdate' : args.startdate,
                               'enddate' : args.enddate,
                               'bin' : 'Kuntavaalit' } )

    # Store results
    # TODO: Store data to database
    outfile = os.path.join('data/', 'incoming',
                           args.startdate.replace(' ', '_') + '-' +
                           args.enddate.replace(' ', '_') + '.csv')
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    open(outfile, 'w').write(r.text)


#
if __name__ == "__main__":
    main(sys.argv[1:])
