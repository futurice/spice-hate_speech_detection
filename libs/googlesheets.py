import gspread
from oauth2client.service_account import ServiceAccountCredentials

def create_google_sheet(sheetname):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('confs/google_sheets.json', scope)
    gc = gspread.authorize(credentials)

    wks = gc.create(sheetname).sheet1

    return wks

def get_access():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('confs/google_sheets.json', scope)
    gc = gspread.authorize(credentials)
    return gc
