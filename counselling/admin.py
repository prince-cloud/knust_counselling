from typing import Sequence
from django.contrib import admin

# Register your models here.
from .models import Counselling, Request, Schedule

admin.site.register(Counselling)
admin.site.register(Request)
admin.site.register(Schedule)
