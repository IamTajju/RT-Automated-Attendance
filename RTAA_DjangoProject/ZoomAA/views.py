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
# Create your views here.

# Global Variable to Store user Response
Response = userResponse()


@allowedUsers(allowedRoles=['Raphael'])
def index(request):

    text = ""
    pathz = ""
    message = ""
    check = ""
    if request.method == "GET":
        request.session["DBWrite"] = False
        Response.reset()

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
                #text = text.encode("ascii", "ignore")
                #text = text.decode()
                Response.addStudentNames(text)
                os.remove(pathz)
            except:
                os.remove(pathz)
                message = "Check your filename and ensure it doesn't have any space or check if it has any text."

        if gradeForm.is_valid():
            Response.grade = gradeForm.cleaned_data["grade"]
            check = "Check Summary"

    return render(request, "ZoomAA/index.html",
                  {
                      "counter": Response.counter,
                      "message": message,
                      "form": GradeForm,
                      "check": check
                  }
                  )


@allowedUsers(allowedRoles=['Raphael'])
def summaryView(request):
    grade = Response.grade
    summary = [[]]
    summary, classDate = updateGSHEETS(Response)

    if request.method == 'POST':
        arr = request.POST.get('arr')
        listOfStudents = list(arr.split(","))
        contactList = contactListOfAbsentees(summary, listOfStudents)
        print(contactList)
        api_key = "C200853760ffa65c04c926.91813669"
        message = f"ur sun/dauter/object missed class"
        response = requests.post(
            f"https://esms.mimsms.com/smsapi?api_key={api_key}&type=text&contacts={contactList}&senderid=RaphaelsPhy&msg={message}")

        print(contactList)
        print(response)

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
