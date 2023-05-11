from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile = models.CharField(max_length=300)
    
    
    def __str__(self):
       return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    #profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"New post: called '{self.title}'"
    
class Reply(models.Model):
    comment = models.CharField(max_length=2000)
    love = models.IntegerField(null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    url = models.CharField(max_length=200)
    userPhoto = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user: {self.user_id} @{self.url}"


# This test class was created to experiment with initial api calls
class Test(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=100)
  def __str__(self):
    return f"This test returned: ${self.name}"
  



