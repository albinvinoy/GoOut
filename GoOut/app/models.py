"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from os.path import splitext

def user_directory_path(instance, filename):
    return 'user/{0}/{1}'.format(instance.user.id,filename)

def profilepic_path(instance, filename):
    return 'user/{0}/profilepic{1}'.format(instance.user.id, splitext(filename)[1])

# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User)
    
    bio = models.CharField(max_length=500)
    profilepic = models.ImageField(upload_to=profilepic_path, blank=True)
