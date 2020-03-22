import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from datetime import datetime

from get_valispace_data import GetValiData

from my_conf import url, project_name, username, password, \
    SPREADSHEET_ID_COST, SPREADSHEET_ID_POWER, \
    SPREADSHEET_ID_MASS, SPREADSHEET_ID_DATA

# # If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def init_google_sheets_api():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickfile = '/Users/Makbukuska/Desktop/Spacecraft_and_Mission_Design/Final_Mission/vali2gsheets/token.pickle'
    credfile = '/Users/Makbukuska/Desktop/Spacecraft_and_Mission_Design/Final_Mission/vali2gsheets/credentials.json'

    if os.path.exists(pickfile):
        with open(pickfile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickfile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def write_last_update_time(service, spreadsheetId):
    values = [
        [
            "Last update ", str(datetime.today().isoformat())
        ],
    ]
    body = {'values': values}

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range='H1:I1',
        valueInputOption='RAW', body=body).execute()


def write_to_google_sheets(info, range, SPREADSHEET_ID, service):
    body = {'values': info}
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range,
        valueInputOption='RAW', body=body).execute()


def update_mass_budget(service, get_vali_data):
    comp_mass_info = get_vali_data.get_comp_mass_info()
    range_comp_mass = 'B3:C11'
    write_to_google_sheets(comp_mass_info, range_comp_mass, SPREADSHEET_ID_MASS, service)

    mass_propulsion_info = get_vali_data.get_propulsion_mass_info()
    range_propulsion_mass = 'B16:C17'
    write_to_google_sheets(mass_propulsion_info, range_propulsion_mass, SPREADSHEET_ID_MASS, service)

    write_last_update_time(service, SPREADSHEET_ID_MASS)


def update_cost_budget(service, get_vali_data):
    comp_cost_info = get_vali_data.get_comp_price_info()
    range_comp_cost = 'B3:B11'
    write_to_google_sheets(comp_cost_info, range_comp_cost, SPREADSHEET_ID_COST, service)

    write_last_update_time(service, SPREADSHEET_ID_COST)


def update_power_budget(service, get_vali_data):
    pass


def update_data_budget(service, get_vali_data):
    payload_data_info = get_vali_data.get_data_payload_info()
    range_payload_data = 'B3:B4'
    write_to_google_sheets(payload_data_info, range_payload_data, SPREADSHEET_ID_DATA, service)

    downlink_data_info = get_vali_data.get_downlink_info()
    range_downlink_data = 'F3:F3'
    write_to_google_sheets(downlink_data_info, range_downlink_data, SPREADSHEET_ID_DATA, service)

    comp_data_info = get_vali_data.get_comp_data_info()
    range_comp_data = 'J4:J5'
    write_to_google_sheets(comp_data_info, range_comp_data, SPREADSHEET_ID_DATA, service)

    time_data_transmitted_to_gs_info = get_vali_data.get_time_data_transmitted_to_gs()
    range_time_data_transmitted_to_gs = 'F5:F5'
    write_to_google_sheets(time_data_transmitted_to_gs_info, range_time_data_transmitted_to_gs, SPREADSHEET_ID_DATA, service)

    orbit_period_info = get_vali_data.get_orbit_period()
    range_orbit_period = 'F11:F11'
    write_to_google_sheets(orbit_period_info, range_orbit_period, SPREADSHEET_ID_DATA, service)

    number_of_gs_info = get_vali_data.get_number_of_gs()
    range_number_of_gs = 'F9:F9'
    write_to_google_sheets(number_of_gs_info, range_number_of_gs, SPREADSHEET_ID_DATA, service)

    write_last_update_time(service, SPREADSHEET_ID_DATA)


def main():
    service = init_google_sheets_api()

    get_vali_data = GetValiData(url, username, password, project_name)

    # ---------------------- UPDATE MASS BUDGET
    update_mass_budget(service, get_vali_data)

    # ---------------------- UPDATE COST BUDGET
    update_cost_budget(service, get_vali_data)

    # ---------------------- UPDATE POWER BUDGET
    update_power_budget(service, get_vali_data)

    # ---------------------- UPDATE DATA BUDGET
    update_data_budget(service, get_vali_data)


main()
