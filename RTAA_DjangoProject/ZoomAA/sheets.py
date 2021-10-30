from __future__ import print_function
from typing import List
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, date
from .helpers import cleaningList, convertDayToLetter, getPresentStudentsIndex, getRedundantColumns


def updateGSHEETS(ZoomNames, Grade):
    # Variables holding scope and cred
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'RTAA_DjangoProject/ZoomAA/keys.json'
    # Account file should be just "ZoomAA/keys.json" in local host
    # SERVICE_ACCOUNT_FILE = 'ZoomAA/keys.json'

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
    grade = Grade
    zoomNameList = ZoomNames

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

    SERVICE_ACCOUNT_FILE = 'ZoomAA/keys.json'
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
    # Redundant Columns are the dates with no classes
    columns = getRedundantColumns(response["values"])
    # Data is cleaned of Redundant Columns
    data = cleaningList(response["values"], columns)
    return data


def GetStudentNames(grade):
    # Variables holding scope and cred
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'RTAA_DjangoProject/ZoomAA/keys.json'
    # Account file should be just "ZoomAA/keys.json" in local host
    # SERVICE_ACCOUNT_FILE = 'ZoomAA/keys.json'

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

    # Get Current Grade's Student Name and Sl.No oh those whose attendance are yet to be updated
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A:{currentDateColumnLetter}", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()

    ListOfList = response["values"]
    listToBeRemoved = []

    for list in ListOfList:
        if (len(list) == (len(ListOfList[0]))):
            listToBeRemoved.append(list)

    for list in listToBeRemoved:
        ListOfList.remove(list)

    # Keeping only Sl No. and Name
    for i in range(len(ListOfList)):
        bufferList = ListOfList[i][0:2]
        ListOfList[i] = bufferList

    return response["values"]


def updateAttendance(StudentIndex, grade, attType):
    # Variables holding scope and cred
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'RTAA_DjangoProject/ZoomAA/keys.json'
    # Account file should be just "ZoomAA/keys.json" in local host
    # SERVICE_ACCOUNT_FILE = 'ZoomAA/keys.json'

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

    # No of Studs to loop through
    numOfStuds = 0

    # Step 1
    '''
    Get Current Grade's Student Name and Sl.No
    '''
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A:{currentDateColumnLetter}", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()
    numOfStuds = len(response["values"]) - 1

    # Step 2
    '''
    Update Current Date's Column's Attendance
    '''

    ListOfList = response["values"]
    attendance_body_value = []

    for i in range(numOfStuds):
        if str((i + 1)) in StudentIndex:
            attendance_body_value.append([str(attType)])

        elif (len(ListOfList[i+1])) == len(ListOfList[0]):
            attendance_body_value.append([str(ListOfList[i+1][-1])])
        else:
            attendance_body_value.append([""])

    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                     range=f"{sheetname}!{currentDateColumnLetter}{2}", valueInputOption="USER_ENTERED", body={"values": attendance_body_value})
    response = request.execute()

    # Step 3 Return Data to view
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                  range=f"{sheetname}!A2:{currentDateColumnLetter}{numOfStuds+1}", valueRenderOption="FORMATTED_VALUE")
    response = request.execute()

    classDateIndex = todays_date.day+2
    return response["values"], classDateIndex
