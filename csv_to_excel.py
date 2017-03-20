#!/usr/local/bin/python3
'''
Hate Speech / CSV to Excel conversion
'''

import sys
import argparse
import os
import glob
import pandas as pd
import xlsxwriter

# Import our custom scripts
sys.path.append('libs/')

DEFAULT_COLUMNS = 'id from_user_name text n_hate_words predicted_label prediced_score'

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir', help='Input directory to be converted', required=True)
    parser.add_argument('--outdir', help='Output directory', required=True)
    parser.add_argument('--cols', help='Columns to include', default=DEFAULT_COLUMNS)
    parser.add_argument('--sortby', help='Row that is going to be used for sorting', default='prediced_score')
    parser.add_argument('--ascending', help='Sort in ascending order (def. False)', default=False)
    parser.add_argument('--newcols', help='Columns to be added', default=['LABEL'])
    args = parser.parse_args(argv)

    # Get a list of files to be converted
    filenames = glob.glob('data/output/*.csv')
    for filename in filenames:
        df = pd.read_csv(filename)

        # Sort the data
        df.sort(args.sortby, ascending=args.ascending, inplace=True)

        # Drop columns that we dont need
        selected_cols = args.cols.split(' ')
        for col in df.columns.tolist():
            if selected_cols.count(col) == 0:
                df.drop(col, axis=1, inplace=True)

        # Add new cols
        for newcol in args.newcols:
            df[newcol] = ''

        # Store file
        outputfile = os.path.join(args.outdir,
                                  '.'.join(os.path.basename(filename).split('.')[:1]) + '.xls')
        if not os.path.exists(os.path.dirname(outputfile)):
            os.makedirs(os.path.dirname(outputfile))
        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        print('Wrote a new excel file: %s' % outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
