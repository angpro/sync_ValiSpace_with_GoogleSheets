# Connect to ValiSpace, retrieve variables and upload to Google Sheets,
# where we can setup nice budget calculations.
# Instructions:
#   1. Setup up Google API to access Google Sheets
#   2. Configure this script to point to files (lines 61, 62)
#         pickfile = '/Users/ ... /token.pickle'
#         credfile = '/Users/... /credentials.json'
#   3. Configure ValiSpace access (line 27)
#   4. Install ValiSpace for python
#           https://github.com/valispace/ValispacePythonAPI
#   5. Configure Google Sheet to be able to accept values
#        Note that there should be worksheet Parameters, or configure the name in line 56
#        Example worksheet: https://docs.google.com/spreadsheets/d/1xzcnTOyD4yMYHcCHYkx2xrpUFYspoT3ykubJ_RSqAT8/edit?usp=sharing
#
# Workflow using this script
#   1. Setup Google Sheet to calculate mass and power budgets.
#   2. Optionally setup data budget (in principle Vali ok) and cost (SSCM is the best choice). In principle, you can add enough variables in the Vali model to have a full data and cost calculations.
#   3. Change subsystem names to what you have in your model. In Google Sheet they're marked with italics font.
#   4. When you need to update your budgets, just run the scropt, it will grab values from vali and forward them to Google Sheets. All of your calculations will be automatically updated.
#
# Version: 1.0, by Anton Ivanov, a.ivanov2@skoltech.ru, 20.03.2020
#
# ------------------------------------------------------------------------------

# See installation instructions at https://github.com/valispace/ValispacePythonAPI
import valispace

import os
import pickle
import sys

# Necessary inputs for the Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from datetime import datetime

# valispace = valispace.API()
# To improve access, one can probably use KeyRing
valispace = valispace.API(url='https://skoltechspacecenter.valispace.com/',
    username='YourUserName', password='YourPassword')

#Get th elist of Vali Components
# This one is not necessary at the moment, we relly need variables in the
# next line. Note this is where you have name your project
projectComps = valispace.get_component_list(project_name='SkolSat')
# Get the list of Vali variables
projectVars = valispace.get_vali_list(project_name='SkolSat')

print('Recived ', len(projectVars), ' valis')

#-----------------------------------------------------------------------------
# Connect to Google Sheets
# You have to get proper credentials first. Follow example at
# https://developers.google.com/sheets/api/quickstart/python
#

# # If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# This ID should contain all of your budget spreadsheets
# It will be more convineint to update all of the parameters at once
SAMPLE_SPREADSHEET_ID = '1xzcnTOyD4yMYHcCHYkx2xrpUFYspoT3ykubJ_RSqAT8'
# Set this range for the worksheet contaning Parametres
# The final range is set to 1000 but there might be more parameters!
# if len(projectVars) > 999 : print ('Change Default range for Google Sheets')
SAMPLE_RANGE_NAME = 'Parameters!A2:F1000'

# Necessary evil to setup Google Sheets
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickfile = '/Users/aivanov/Documents/Projects/MARSIS/token.pickle'
    credfile = '/Users/aivanov/Documents/Projects/MARSIS/credentials.json'

    if os.path.exists( pickfile ):
        with open( pickfile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open( pickfile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
# Create list of variables to upload to Google Sheets

    values = []
    for d in projectVars:
        values.append( [ d['id'], d['parent'], d['name'], d['value'], d['margin_plus'], d['unit'] ]);

    body = { 'values': values }

    result = service.spreadsheets().values().update(
         spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
         valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

# Add current date
    values = [
        [
           "Last update ", str(datetime.today().isoformat())
        ],
              ]
    body = { 'values': values }

    result = service.spreadsheets().values().update(
         spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Parameters!H2:I2',
         valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
