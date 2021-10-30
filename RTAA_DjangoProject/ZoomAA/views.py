from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from .decorators import *
import pytesseract
from .forms import GradeForm, ImageUpload
from .helpers import *
import requests
from PIL import Image
from django.conf import settings
from .sheets import *
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
# Create your views here.


@allowedUsers(allowedRoles=['Raphael'])
def index(request):
    grades = [["9 Online", "9 Bashundhara", "9 Uttara"], ["10 Online", "10 Bashundhara", "10 Uttara"], [
        "11 Online", "11 Bashundhara", "11 Uttara"], ["12 Online", "12 Bashundhara", "12 Uttara"]]

    request.session["message"] = ""
    return render(request, "ZoomAA/index.html", {
        "grades": grades
    })


def AttendanceInput(request, grade):
    data = GetStudentNames(grade)
    if request.method == 'POST':
        # Get List of checked students' index to see who are present and absent
        arr = request.POST.get('arr')

        PresentStudentIndex = getStudentsIndexList(
            list(arr.split(",")), "Present")
        AbsentSMSStudentIndex = getStudentsIndexList(
            list(arr.split(",")), "AbsentSMS")
        AbsentStudentIndex = getStudentsIndexList(
            list(arr.split(",")), "Absent")

        summary, classDate = updateAttendance(
            PresentStudentIndex, grade, "Present")

        summary, classDate = updateAttendance(
            AbsentSMSStudentIndex, grade, "Absent")

        summary, classDate = updateAttendance(
            AbsentStudentIndex, grade, "Absent")

        # Gets seperate contact list for absent and present students
        absenteeContacts, presentContacts = createContactList(
            summary, PresentStudentIndex, AbsentSMSStudentIndex)

        # Api Key for SMS
        api_key = "C200853760ffa65c04c926.91813669"

        # Console print for check
        print("A:" + absenteeContacts)
        print("P:" + presentContacts)

        # Setting date and time to send as a part of SMS
        dateToday = str(date.today())
        now = datetime.now() + timedelta(hours=6)
        current_time = now.strftime("%H:%M:%S")

        # Console print to check time and date
        print(f"SMS Sent on: {current_time}")

        # Message bodies
        Absentmessage = f"Greetings! Your child is absent in today's online physics class with Raphael Sir. As noted on {dateToday} at {current_time}. We are requesting you to take appropriate action in this regard. ধন্যবাদ।"
        Presentmessage = f"Greetings! Your child is present in today's online physics class with Raphael Sir. As noted on {dateToday} at {current_time}. ধন্যবাদ।"

        # Making API calls for absent students
        response = requests.post("https://esms.mimsms.com/smsapi",
                                 {
                                     "api_key": api_key,
                                     "type": "text",
                                     "contacts": f"{absenteeContacts}",
                                     "senderid": "RaphaelsPhy",
                                     "msg": f"{Absentmessage}"
                                 })

        # Console print to check if API call was successful
        absent_status_code = response.status_code
        print(f"Absent API Call: {absent_status_code}")

        # Making API calls for present students
        response = requests.post("https://esms.mimsms.com/smsapi",
                                 {
                                     "api_key": api_key,
                                     "type": "text",
                                     "contacts": f"{presentContacts}",
                                     "senderid": "RaphaelsPhy",
                                     "msg": f"{Presentmessage}"
                                 })
        present_status_code = response.status_code
        print(f"Present API Call: {present_status_code}")
        if ((present_status_code == 200)) and ((absent_status_code == 200)):
            message = "SMS sent out successfully"
        else:
            message = "You messed up boi, try again."

        request.session["message"] = message

    return render(request, "ZoomAA/attendanceInput.html", {
        "data": data,
        "grade": grade,
        "message": request.session["message"]
    })


@allowedUsers(allowedRoles=['Raphael'])
def onlineIndex(request):

    text = ""
    message = ""
    check = ""
    if request.method == "GET":
        request.session["ZoomNames"] = []
        request.session["Grade"] = "9"
        request.session["counter"] = 0

    if request.method == "POST":
        form = ImageUpload(request.POST, request.FILES)
        gradeForm = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                image = request.FILES['image']
                pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
                # Change to 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' in localhost
                # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
                text = pytesseract.image_to_string(
                    Image.open(image), lang='eng')
                text = text.encode("ascii", "ignore")
                text = text.decode()
                bufferList = text.split("\n")
                request.session["ZoomNames"] = request.session["ZoomNames"] + bufferList
                request.session["counter"] = request.session["counter"] + 1
                message = request.session["ZoomNames"]
            except:
                message = "Check your filename and ensure it doesn't have any space or check if it has any text."

        if gradeForm.is_valid():
            message = request.session["ZoomNames"]
            request.session["Grade"] = gradeForm.cleaned_data["grade"]
            check = "Check Summary"

    return render(request, "ZoomAA/onlineIndex.html",
                  {
                      "counter": request.session["counter"],
                      "message": message,
                      "form": GradeForm,
                      "check": check
                  }
                  )


@allowedUsers(allowedRoles=['Raphael'])
def summaryView(request):
    grade = request.session["Grade"]
    summary = [[]]
    ZoomNames = request.session["ZoomNames"]
    summary, classDate = updateGSHEETS(
        ZoomNames, grade)

    if request.method == 'POST':
        # Get List of checked students' index to see who are present and absent
        arr = request.POST.get('arr')
        # Splits the string with assigned delimiter
        listOfStudents = list(arr.split(","))

        # Gets seperate contact list for absent and present students
        absenteeContacts, presentContacts = createContactList(
            summary, listOfStudents)

        # Api Key for SMS
        api_key = "C200853760ffa65c04c926.91813669"

        # Console print for check
        print("A:" + absenteeContacts)
        print("P:" + presentContacts)

        # Setting date and time to send as a part of SMS
        dateToday = str(date.today())
        now = datetime.now() + timedelta(hours=6)
        current_time = now.strftime("%H:%M:%S")

        # Console print to check time and date
        print(f"SMS Sent on: {current_time}")

        # Message bodies
        Absentmessage = f"Greetings! Your child is absent in today's online physics class with Raphael Sir. As noted on {dateToday} at {current_time}. We are requesting you to take appropriate action in this regard. ধন্যবাদ।"
        Presentmessage = f"Greetings! Your child is present in today's online physics class with Raphael Sir. As noted on {dateToday} at {current_time}. ধন্যবাদ।"

        # Making API calls for absent students
        response = requests.post("https://esms.mimsms.com/smsapi",
                                 {
                                     "api_key": api_key,
                                     "type": "text",
                                     "contacts": f"{absenteeContacts}",
                                     "senderid": "RaphaelsPhy",
                                     "msg": f"{Absentmessage}"
                                 })

        # Console print to check if API call was successful
        print(f"Absent API Call: {response}")
        print(type(response))

        # Making API calls for present students
        response = requests.post("https://esms.mimsms.com/smsapi",
                                 {
                                     "api_key": api_key,
                                     "type": "text",
                                     "contacts": f"{presentContacts}",
                                     "senderid": "RaphaelsPhy",
                                     "msg": f"{Presentmessage}"
                                 })
        print(f"Present API Call: {response}")

    return render(request, "ZoomAA/summary.html",
                  {
                      "Grade": grade,
                      "summary": summary,
                      "classDate": classDate,
                  }
                  )


@allowedUsers(allowedRoles=['Raphael'])
def history(request):
    data9 = getHistoricalAttendance("9")
    data10 = getHistoricalAttendance("10")
    data11 = getHistoricalAttendance("11")
    data12 = getHistoricalAttendance("12")
    return render(request, "ZoomAA/at.html", {
        "data9": data9[1:len(data9)-1],
        "row9": data9[0],
        "data10": data10[1:len(data10)-1],
        "row10": data10[0],
        "data11": data11[1:len(data11)-1],
        "row11": data11[0],
        "data12": data12[1:len(data12)-1],
        "row12": data12[0],
    })


@unauthenticated
def loginView(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "ZoomAA/login.html", {
                "message": "Invalid credentials"
            }
            )
    else:
        return render(request, "ZoomAA/login.html")


def logoutView(request):

    logout(request)

    return render(request, "ZoomAA/login.html", {
        "message": "Logged Out."
    }
    )
