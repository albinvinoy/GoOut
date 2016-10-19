"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from os.path import splitext
import uuid

def user_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.id,filename)

def profilepic_path(instance, filename):
    id=uuid.uuid4().urn[9:]
    return 'user/{0}/profilepic-{1}{2}'.format(instance.user.id, id, splitext(filename)[1])

# Create your models here.
class Interest(models.Model):
    name=models.CharField(max_length=100)

class UserInfo(models.Model):
    user = models.ForeignKey(User)
    
    admin = models.BooleanField(default=False)
    bio = models.CharField(max_length=500)
    profilepic = models.ImageField(upload_to=profilepic_path, blank=True)
    interests=models.ManyToManyField(Interest, through='UserInterest')

class UserInterest(models.Model):
    user=models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    interest=models.ForeignKey(Interest, on_delete=models.CASCADE)

    priority=models.IntegerField()