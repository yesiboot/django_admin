from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    job = models.TextField(max_length= 100, default= "")
    bio = models.CharField(max_length= 200, default= "")
