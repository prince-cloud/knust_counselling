from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from .models import CustomUser, Programme, Student, College
from allauth.account.forms import SignupForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'gender', 'profile_picture',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')
        exclude = ('password',)


class SignupForm(SignupForm):
    GENDER_CHOICE = [
    ("Male", "Male"),
    ("Female", "Female"),
    ]
    phone_number = forms.CharField(max_length=10, label="Phone #")
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    profile_picture = forms.ImageField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    def __init__(
        self, data=None, initial=None, *args, **kwargs):
        super(SignupForm, self).__init__(
            data=data, initial=initial, *args, **kwargs
        )

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.is_student = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.gender = self.cleaned_data['gender']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.save()
        return user


class StudentSignUpForm(forms.ModelForm):
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
    )
    programme = forms.ModelChoiceField(
        queryset=Programme.objects.all()
    )

    class Meta:
        model = Student
        fields = (
            "student_id",
            "index_number",
            "college",
            "programme",
            "year",
            "hall_of_affiliation",
        )

    def __init__(
        self, data=None, instance=None, initial=None, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(
            data=data, instance=instance, initial=initial, *args, **kwargs
        )
        if not instance and not data:
            if initial:
                college = initial.get("college")
                if college:
                    self.fields["programme"].queryset = Programme.objects.filter(
                        college=college
                    )
                else:
                    self.fields["programme"].queryset = Programme.objects.all()
            else:
                self.fields["programme"].queryset = Programme.objects.all()

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        p = data["password2"]
        p_1 = data["password"]
        if len(p) < 6:
            raise forms.ValidationError("Your password should be 6 or more characters")
        if p == p_1:
            return p
        raise forms.ValidationError("Your passwords do not match")
    
    def clean_index_id(self, *args, **kwargs):
        data = self.cleaned_data
        student_id = data["student_id"]
        index_number =data["index_number"]
        if len(student_id) < 8:
            raise forms.ValidationError("Inccorect Student ID. Shoould be 8 characters")
        if len(index_number) < 7:
            raise forms.ValidationError("Inccorect Index Number. Shoould be 7 characters")