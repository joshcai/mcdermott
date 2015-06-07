from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserInfo(models.Model):
  user = models.OneToOneField(User)
  utd_id = models.CharField(max_length=50)
  major = models.CharField(max_length=200)
  major2 = models.CharField(max_length=200)
  minor = models.CharField(max_length=200)
  minor2 = models.CharField(max_length=200)
  hometown = models.CharField(max_length=200)
  high_school = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=200)
  #TODO: add address field
  #TODO: allow multiple phone
  #TODO: allow backup emails
