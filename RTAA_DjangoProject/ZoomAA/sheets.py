from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, date
from .helpers import cleaningList, convertDayToLetter, getPresentStudentsIndex, getRedundantColumns


def updateGSHEETS(Response):
    # Variables holding scope and cred
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # Account file should be just "ZoomAA/keys.json" in local host
    SERVICE_ACCOUNT_FILE = 'RTAA_DjangoProject/ZoomAA/keys.json'

    # Setting creds
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1N2Oyd4J2qhYeJ1_adDAPfl2lHFM2WuMmYK83Tb_1i7g'
    service = build('sheets', 'v4', credentials=creds)

    # Getting today's date and current month
    todays_date = date.today()
    month = str(datetime.now().strftime('%B'))
    currentDateColumnLetter = convertDayToLetter(todays_date.day)

    # Response from Homepage
    grade = Response.grade
    zoomNameList = Response.studentNames

    # Sheet Name to be used
    sheetname = month+str(grade)

    # No of Studs to loop through
    numOfStuds = 0

    # Step 1
    '''
    Get Current Grade's Student Name and Sl.No
    '''
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A:B", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()
    numOfStuds = len(response["values"]) - 1

    presentStudentIndices = []
    presentStudentIndices = getPresentStudentsIndex(
        zoomNameList, response["values"])

    # Step 2
    '''
    Update Current Date's Column's Attendance
    '''

    absent_body_value = []
    for i in range(numOfStuds):
        if (i + 1) in presentStudentIndices:
            absent_body_value.append(["Present"])
        else:
            absent_body_value.append(["Absent"])

    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                     range=f"{sheetname}!{currentDateColumnLetter}{2}", valueInputOption="USER_ENTERED", body={"values": absent_body_value})
    response = request.execute()

    # Step 3 Return Data to view
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A2:{currentDateColumnLetter}{numOfStuds+1}", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()

    classDateIndex = todays_date.day+2
    return response["values"], classDateIndex


def getHistoricalAttendance(grade):
    # Variables holding scope and cred
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # Account file should be just "ZoomAA/keys.json" in local host
    SERVICE_ACCOUNT_FILE = 'RTAA_DjangoProject/ZoomAA/keys.json'

    # Setting creds
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1N2Oyd4J2qhYeJ1_adDAPfl2lHFM2WuMmYK83Tb_1i7g'
    service = build('sheets', 'v4', credentials=creds)

    # Getting today's date and current month
    todays_date = date.today()
    month = str(datetime.now().strftime('%B'))
    currentDateColumnLetter = convertDayToLetter(todays_date.day)

    # Sheet Name to be used
    sheetname = month+str(grade)
    # Step 1
    '''
    Get Selected Grade's Month's Attendance
    '''
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A1:{currentDateColumnLetter}", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()
    columns = getRedundantColumns(response["values"])
    data = cleaningList(response["values"], columns)
    return data
