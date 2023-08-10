from __future__ import print_function

import os.path

from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# SPREADSHEET_ID = '1skyShVYTw5frwJLXJMskpzOXN45WaNpxEN7cuOkZtnY'
SPREADSHEET_ID = '1LZkrX7-WutUBfezaLusgnOWHy_G7x4kujXKl3ym4LjU'

class Editor:
    def __init__(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            self.sheet = service.spreadsheets()

            

        except HttpError as err:
            print(err)
    def xl_rowcol_to_cell(self, row_num, col_num):
        col_str = ''

        # Removed these 2 lines if your row, col is 1 indexed.
        row_num += 1
        col_num += 1

        while col_num:
            remainder = col_num % 26

            if remainder == 0:
                remainder = 26

            # Convert the remainder to a character.
            col_letter = chr(ord('A') + remainder - 1)

            # Accumulate the column letters, right to left.
            col_str = col_letter + col_str

            # Get the next order of magnitude.
            col_num = int((col_num - 1) / 26)

        return col_str + str(row_num)

    def update(self, range, values):
        self.sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption="USER_ENTERED", body={'values' : values}).execute()

    def updateCoord(self, x, y, values):
        self.update(self.xl_rowcol_to_cell(y, x), values)
    
    def read(self, range):
        return self.sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute().get('values', [])

    def readCoord(self, x, y):
        return self.read(self.xl_rowcol_to_cell(y, x))
    
    def get_names_dict(self):
        return {b:a+3 for a, b in enumerate(self.read('D1:1')[0])}

    def get_dates_dict(self):
        dic = {b[0]:a for a, b in enumerate(self.read('B1:B')) if len(b) > 0}
        for key, value in list(dic.items()):
            try:
                datetime.strptime(key, "%d/%m/%y")
            except:
                del dic[key]
        
        return dic

    def set(self, name, date):
        names_dict = self.get_names_dict()
        dates_dict = self.get_dates_dict()

        if name in names_dict:
            print("Index to update is ", names_dict[name], dates_dict[date])
        else:
            newX = max(list(names_dict.values())) + 1
            print("New name entry at ", newX, 0)
            print("Index to update is ", newX, dates_dict[date])


editor = Editor()
editor.set('fds', '07/08/23')