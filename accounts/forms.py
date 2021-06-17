from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from .models import CustomUser
from allauth.account.forms import SignupForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'gender', 'profile_picture',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


""" class SignupForm(SignupForm):
    GENDER_CHOICE =[
    ("Male", "Male"),
    ("Female", "Female"),
    ]
    phone_number = forms.CharField(max_length=10, label="Phone #")
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    profile_picture = forms.ImageField()

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.gender = self.cleaned_data['gender']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.save()
        return user """



class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label="Re-enter password", widget=forms.PasswordInput)
    password = forms.CharField(
        widget=forms.PasswordInput, help_text="must be more than 6 characters"
    )
    #username = forms.CharField(
    #    help_text="case sensitive",
    #)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
            "password",
        )

    def __init__(
        self, data=None, instance=None, initial=None, *args, **kwargs):
        super(RegisterForm, self).__init__(
            data=data, instance=instance, initial=initial, *args, **kwargs
        )

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        p = data["password2"]
        p_1 = data["password"]
        if len(p) < 6:
            raise forms.ValidationError("Your password should be 6 or more characters")
        if p == p_1:
            return p
        raise forms.ValidationError("Your passwords do not match")

