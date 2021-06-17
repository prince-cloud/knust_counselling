from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import College
from django.urls import reverse

# Create your models here.
COUNSELLING_MODE = [
    ("Online", "Online"),
    ("In-Person", "In-Person"),
]

class Counselling(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ("name",)
    def __str__(self):
        return self.name

class Request(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    counselling_type = models.ForeignKey(Counselling, on_delete=models.SET_NULL, null=True)
    counselling_mode = models.CharField(choices=COUNSELLING_MODE, max_length=50)
    message = models.TextField()
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    viewed = models.BooleanField(default=False)
    scheduled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)
    
    def __str__(self):
        return self.user.username
    
    def get_requests(self) -> str:
        return reverse("counselling:counselling_requests")
        #return reverse("shop:product_detail", kwargs={"slug": self.slug})

class Schedule(models.Model):
    counselor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="counselor_schedule")
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    counselling_mode = models.CharField(choices=COUNSELLING_MODE, max_length=100)
    message = models.TextField(null=True)
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)