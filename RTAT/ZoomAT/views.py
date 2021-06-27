from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
import base64

# Create your views here.


def base64_encode(string):
    data = string
    # Standard Base64 Encoding
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return encodedStr


def index(request):
    return render(request, "ZoomAT/index.html")


def zoom_callback(request):
    code = request.GET["code"]
    data = requests.post(f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://127.0.0.1:8000/ZoomAT/", headers={
        "Authorization": "Basic" + base64_encode("ixf2WyJdR1exUEFjXlcJQQ:0Y3xgJLrmnZh94FgDgy7oCHPb8V3KcKl")
    }
    )
    requests.session["zoom_access_token"] = data.json()["access_token"]
    print(data)
    return HttpResponseRedirect("/ZoomAT/")
