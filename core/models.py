from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserInfo(models.Model):
  user = models.OneToOneField(User)
  utd_id = models.CharField(max_length=50, blank=True)
  major = models.CharField(max_length=200, blank=True)
  major2 = models.CharField(max_length=200, blank=True)
  minor = models.CharField(max_length=200, blank=True)
  minor2 = models.CharField(max_length=200, blank=True)
  hometown = models.CharField(max_length=200, blank=True)
  high_school = models.CharField(max_length=200, blank=True)
  phone_number = models.CharField(max_length=200, blank=True)
  #TODO: add address field
  #TODO: allow multiple phone
  #TODO: allow backup emails
