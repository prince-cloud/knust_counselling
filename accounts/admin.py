from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Hall, Programme, Student, Counsellor, College

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','email', 'phone_number',]
    fieldsets = [
        *UserAdmin.fieldsets,
    ]
    fieldsets.insert(
        1,
        (
            "Profile Information",
            {
                "fields": (
                    "phone_number",
                    "profile_picture",
                    "gender",
                    "is_student",
                    "is_counselor",
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Student)

admin.site.register(Counsellor)

admin.site.register(College)
admin.site.register(Hall)
admin.site.register(Programme)

