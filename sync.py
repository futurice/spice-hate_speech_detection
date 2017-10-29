#!/usr/local/bin/python3
'''
Hate Speech / Sync
Syncs local database with Google Sheets
'''

import sys
import argparse
import os
import glob

# Import our custom scripts
sys.path.append('libs/')
import googlesheets

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir', help='Input directory to sync with Google Drive', required=True)
    parser.add_argument('--force', help='Force syncing to Google Drive', default=False)
    args = parser.parse_args(argv)

    #
    gc = googlesheets.get_access()

    # Get a list of sheets in Google Drive
    spreadsheets = gc.openall()

    print('%d sheets in Google drive to be synced' % len(spreadsheets))

    # Keep a list of sheets in Google Drive so we dont upload a new document
    # over the old one
    synced_sheets = []

    # Copy annnotations from each file to local storage
    for sh in spreadsheets:
        synced_sheets.append(sh.title)
        headers = sh.sheet1.row_values(1)
        #annotations = sh.sheet1.col_values(headers.index('LABEL') + 1)
        #message_ids = sh.sheet1.col_values(headers.index('id') + 1)
        # TODO: Write the logic to update local storage

    # Sync missing files to Google Drive
    filenames = glob.glob('data/output/*.csv')
    for filename in filenames:
        basename = os.path.basename(filename)

        # If the file is not synced yet, then upload a new file
        if (synced_sheets.count(basename) == 0) or args.force:

            if (synced_sheets.count(basename) == 1) and args.force:
                print('Force syncing %s' % filename)
                sh = gc.open(basename)
            else:
                # Create a new sheet
                sh = gc.create(basename)

            # Import new data from CSV
            gc.import_csv(sh.id, open(filename, 'r').read())
            # Share the document to get access to it
            sh.share('teemu.kinnunen@futurice.com', perm_type='user', role='writer')
            # Add a new column and name it to hatespeech_label
            headers = sh.sheet1.row_values(1)
            sh.sheet1.update_cell(1, headers.index('prediced_score') + 2,
                                  'hatespeech_label')

if __name__ == "__main__":
    main(sys.argv[1:])
