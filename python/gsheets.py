### Imports Libraries and methods to Initialize Google Sheets API Service
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_gsheet(sheet_name):
    # Initializes Google Sheets API Service from client
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('********************.json', scope) # Credentials JSON from GCP
    client = gspread.authorize(creds)

    # Obtains a Google Sheets service
    sheet = client.open(sheet_name).sheet1
    print("Defined Google Sheets Service")

    return sheet