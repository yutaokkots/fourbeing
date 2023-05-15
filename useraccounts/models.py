from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    bio = models.CharField(max_length=200)
    location = models.CharField(max_length=75)
    website = models.CharField(max_length=100)
    
    def __str__(self):
       return self.user.username
    

class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"Photo for user: {self.user_id} @{self.url}"
