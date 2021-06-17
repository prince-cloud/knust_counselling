from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelState

YEAR_CHOICE = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
]
GENDER_CHOICE =[
    ("Male", "Male"),
    ("Female", "Female"),
]

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    profile_picture = models.ImageField(upload_to="profile_pictures/")

    is_student = models.BooleanField(default=False)
    is_counselor = models.BooleanField(default=False)
    

    def __str__(self):
        return self.get_full_name()

class College(models.Model):
    """
    A representation of a College
    """

    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="college_logo/")

    def __str__(self) -> str:
        return self.name

class Programme(models.Model):
    """
    A representation of all programmes. 

    Intended to hold all programmes offered inn the school
    """
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, related_name="programmes", on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

class Hall(models.Model):
    """
    A representation of all Halls. 

    This includes school halls and hostels
    """

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Counsellor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="counselor")
    college = models.ForeignKey(College, related_name="counsellers", on_delete=models.SET_NULL, null=True)
    bio = models.TextField()

    def __str__(self):

        return " ".join([self.user.first_name, self.user.last_name])


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student")
    student_id = models.CharField(max_length=8, )
    index_number = models.CharField(max_length=7)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="students")
    year = models.CharField(choices=YEAR_CHOICE, max_length=5)
    college = models.ForeignKey(College, blank=True, on_delete=models.CASCADE, related_name="students")
    hall_of_affiliation = models.ForeignKey(Hall, related_name="students", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return " ".join([self.user.first_name, self.user.last_name])