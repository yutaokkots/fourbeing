from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    profile = models.CharField(max_length=100)
    

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__ (self):
        return f"New post: called {self.title} by {self.profile.username}"
    
class Reply(models.Model):
    comment = models.CharField(max_length=2000)
    love = models.IntegerField(null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

