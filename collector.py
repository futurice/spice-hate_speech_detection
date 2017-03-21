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
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd

sys.path.append('confs')
import hiit_collector

def fetch_data(api_key, candidate_data_gdocs, gdocs_key, startdate, enddate):

    data = []

    credentials = ServiceAccountCredentials.from_json_keyfile_name( gdocs_key, ['https://spreadsheets.google.com/feeds'] )

    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url( candidate_data_gdocs ).sheet1

    candidates = sheet.get_all_records( True )

    twitter = map( lambda x: x['twitter'].lower(), candidates )
    twitter = filter( lambda x: x != 'na', twitter )

    for candidate in twitter:

        params = {
            'api_search[query]' : 'type:twitter_tweet AND author:' + candidate,
            'api_key' : api_key,
            'api_search[limit]': 5000
        }

        url = 'https://api.futusome.com/api/searches.json'

        print( params )
        print( url )

        r = requests.get(url, params = params )

        j = r.json()

        if 'documents' in j: ## there can be a lot of errors

            print( candidate, len( j['documents'] ) ) ## make easier to debug

            data += j['documents']

    ## formulate back into CSV type of format
    data = map( lambda entry: entry['fields'] , data )

    return list( data )

def store_messages(cvsstr, filename):

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    open(outfile, 'w').write(csvstr)

def main(argv):
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='API key')
    parser.add_argument('--candidate_data', help='GDocs URL for data')
    parser.add_argument('--google_keys', help='GDocs URL keys')
    parser.add_argument('--outdir', help='Directory to store data')
    parser.add_argument('--startdate', help='Startdate as YYYY-MM-DD')
    parser.add_argument('--enddate', help='Enddate as YYYY-MM-D')

    args = parser.parse_args(argv)

    #TODO: Change it that it get everything unless user sets start and end

    if args.key is None:
        args.key = hiit_collector.api_key
    if args.candidate_data is None:
        args.candidate_data = hiit_collector.candidate_gdocs
    if args.google_keys is None:
        args.google_keys = hiit_collector.candidate_gdocs_keys

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
            response = fetch_data( args.key, args.candidate_data, args.google_keys, startdate_str , enddate_str )

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
