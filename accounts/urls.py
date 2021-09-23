from django.urls import path, include, re_path
from . import views

app_name = "accounts"

path = [
    path("accounts/student/register/", views.student_signup, name="student_signup"),

]