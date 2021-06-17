from django.urls import path, include, re_path
from . import views

app_name = "counselling"

urlpatterns = [
    path("", views.index, name="index"),
    path("requests/", views.counselling_requests, name="counselling_requests"),
    path("make-requests/", views.make_request, name="make_request"),
    path("schedule/request/<int:id>/", views.schedule_request, name="schedule_request"),
    path("re-schedule/request/<int:id>/", views.reschudle_appointment, name="reschudle_appointment"),
    path("view/request/<int:id>/", views.view_counselling_request, name="view_counselling_request"),
    path("my-schedules/", views.my_schedules, name="my_schedules"),
    path("my-requests/", views.my_requests, name="my_requests"),
    path("delete-appointment/<int:id>/", views.delete_appointment, name="delete_appointment"),
]