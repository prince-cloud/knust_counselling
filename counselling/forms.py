from django import forms
from django.db.models import fields
from .models import Schedule, Request
from django.contrib.admin import widgets

class DateInput(forms.DateTimeInput):
    input_type = "datetime-local"


class ScheduleForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=DateInput,
        label="Appointment Date",
    )

    message = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows':3,})
    )
    class Meta:
        model = Schedule
        fields = (
            "counselling_mode",
            "date",
            "message",
        )

class RequestForm(forms.ModelForm):
    message = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows':3,})
    )
    
    class Meta:
        model = Request
        fields = (
            "counselling_type",
            "message",
            "counselling_mode",
        )