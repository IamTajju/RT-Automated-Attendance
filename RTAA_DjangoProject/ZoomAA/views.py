from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from .decorators import *
import pytesseract
from .forms import GradeForm, ImageUpload
from .helpers import *
import os
import requests
from PIL import Image
from django.conf import settings
from .sheets import *
from datetime import date
from datetime import datetime
# Create your views here.

# Global Variable to Store user Response
# Response = userResponse()


@allowedUsers(allowedRoles=['Raphael'])
def index(request):

    text = ""
    #pathz = ""
    message = ""
    check = ""
    if request.method == "GET":
        request.session["DBWrite"] = False
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
                '''
                    image = image.name
                    path = settings.MEDIA_ROOT
                    # "\\images\\" for local host
                    pathz = path + "/images/" + image
                    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
                    # C:\\Program Files\\Tesseract-OCR\\tesseract.exe
                    
                image = image.name
                path = settings.MEDIA_ROOT
                pathz = path + "/images/" + image
                '''
                pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
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

    return render(request, "ZoomAA/index.html",
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
        arr = request.POST.get('arr')
        listOfStudents = list(arr.split(","))
        absenteeContactList, presentContactList = contactListOfAbsentees(
            summary, listOfStudents)
        api_key = "C200853760ffa65c04c926.91813669"
        dateToday = str(date.today())
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        Absentmessage = f"Greetings! Your child is absent in today's online physiscs class with Raphael Sir. As noted on {dateToday} at {current_time}. We are requesting you to take appropriate action in this regard."
        Presentmessage = f"Greetings! Your child is present in today's online physiscs class with Raphael Sir. As noted on {dateToday} at {current_time}."
        response = requests.post(
            f"https://esms.mimsms.com/smsapi?api_key={api_key}&type=text&contacts={absenteeContactList}&senderid=RaphaelsPhy&msg={Absentmessage}")

        response = requests.post(
            f"https://esms.mimsms.com/smsapi?api_key={api_key}&type=text&contacts={presentContactList}&senderid=RaphaelsPhy&msg={Presentmessage}")

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
