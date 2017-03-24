#!/usr/local/bin/python3
'''

This script predicts/detects hate speech for new messages

'''
import requests
import argparse
import sys
from io import StringIO
import datetime
from calendar import monthrange
import os

import csv
import json
import bs4
import dateparser
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd

sys.path.append('confs')
import hiit_collector

def fetch_data(username, password, hostname, paths, startdate, enddate):

    ## twitter data collection

    data = ''

    print( 'Collecting', paths[0] )

    url = 'http://' + username + ':' + password + '@' + hostname + '/' + paths[0][0]
    r = requests.get(url,
                     params = {'resource': 'querybin/tweets',
                               'action' : 'tweet-export',
                               'startdate' : startdate,
                               'enddate' : enddate,
                               'bin' : paths[0][1] } )

    data += r.text

    for path in paths[1:]:

        print( 'Collecting', path )

        url = 'http://' + username + ':' + password + '@' + hostname + '/' + path[0]
        r = requests.get(url,
                         params = {'resource': 'querybin/tweets',
                                   'action' : 'tweet-export',
                                   'startdate' : startdate,
                                   'enddate' : enddate,
                                   'bin' : path[1] } )

        d = r.text.split('\n')[1:]
        data += '\n'.join( d )


    ## remove as much identification as possible
    data = csv.DictReader( StringIO( data ) )

    candidates = open('candidates_twitter_accounts.txt').readlines()
    candidates = list( map( lambda x: x.strip().lower(), candidates ) )

    data_cleaned_twitter = []
    for d in data:

        ## only explore candidates!!!
        if d['from_user_name'].lower() in candidates:

            data_cleaned_twitter.append( {
                'source' : 'twitter',
                'id' : d['\ufeffid'],
                'text' : d['text'],
                'created_at' : d['created_at']
            } )

    print( 'Total', len( data_cleaned_twitter )  )

    ## facebook data collection

    url = 'http://' + username + ':' + password + '@' + hostname + '/vaalitfb/'

    r = requests.get( url )
    soup = bs4.BeautifulSoup( r.text,  'html5lib' )

    data = []

    ## update dates to datetim
    startdate = dateparser.parse( startdate )
    enddate = dateparser.parse( enddate )

    ## todo: add time filtering
    for f in soup.find_all('a'):
        f = f['href']

        if f.endswith('.json') and '_' not in f:
            try:
                print( 'Collecting' , f )
                r = requests.get( url + f )
                r = r.json()
                r = r['feed']
                ## limit to selected dates

                added = 0
                for post in r:
                  if startdate <= dateparser.parse( post['created_time'] ) <= enddate:
                     data.append( post )
                     added += 1

                print( added )

            except Exception as e:
                print("Failed with", f, "caused by", e)

    data_cleaned_fb = []

    ## remove identification when possible
    for d in data:
        msg = ''
        if 'message' in d:
            msg = d['message']
        data_cleaned_fb.append({
            'source' : 'facebook',
            'id' : d['id'],
            'text' : msg, ## xxx? potentially breaks
            'created_at' : d['created_time']
        })

    return data_cleaned_twitter + data_cleaned_fb

def store_messages(cvsstr, filename):

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    open(outfile, 'w').write(csvstr)

def main(argv):
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--hostname', help='Hostname')
    parser.add_argument('--paths', help='list of paths and bin names')
    parser.add_argument('--outdir', help='Directory to store data')
    parser.add_argument('--startdate', help='Startdate as YYYY-MM-DD')
    parser.add_argument('--enddate', help='Enddate as YYYY-MM-DD')

    args = parser.parse_args(argv)

    #TODO: Change it that it get everything unless user sets start and end


    if args.user is None:
        args.user = hiit_collector.username
    if args.password is None:
        args.password = hiit_collector.password
    if args.hostname is None:
        args.hostname = hiit_collector.hostname
    if args.paths is None:
        args.paths = hiit_collector.paths
    if args.startdate is None:
        startdate = datetime.datetime.now() #.strftime('%Y-%m-%d 00:00:00 utc')
    else:
        startdate = datetime.datetime.strptime(args.startdate, '%Y-%m-%d').date()
    if args.enddate is None:
        enddate = datetime.datetime.now() #.strftime('%Y-%m-%d 23:59:59 utc')
    else:
        enddate = datetime.datetime.strptime(args.enddate, '%Y-%m-%d').date()

    print(startdate, enddate)

    for m in range(startdate.month, enddate.month + 1):
        # Get the day range
        if m == enddate.month:
            days = range(startdate.day, enddate.day + 1)
        else:
            _, days = monthrange(startdate.year, m)
        print(days)

        for d in days:
            startdate_str = '%d-%02d-%02d 00:00:00 utc' % (startdate.year, m, d)
            enddate_str = '%d-%02d-%02d 23:59:59 utc' % (startdate.year, m, d)

            print(startdate_str, enddate_str)

            # Get the data

            response = fetch_data( args.user, args.password, args.hostname, args.paths, startdate_str , enddate_str )

            # Store results
            # TODO: Store data to database
            outfile = os.path.join('data/', 'incoming',
                                   startdate_str.replace(' ', '_') + '.json')
            if not os.path.exists(os.path.dirname(outfile)):
                os.makedirs(os.path.dirname(outfile))
            json.dump( response, open(outfile, 'w') )


#
if __name__ == "__main__":
    main(sys.argv[1:])
