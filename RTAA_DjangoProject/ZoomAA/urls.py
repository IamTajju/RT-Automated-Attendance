from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("attendanceInput/<str:grade>",
         views.AttendanceInput, name="attendanceInput"),
    path("online", views.onlineIndex, name="onlineIndex"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("summary", views.summaryView, name="summary"),
    path("history", views.history, name="history"),
]
