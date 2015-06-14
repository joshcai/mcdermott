from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class McUser(models.Model):
  """Fields from default User model:
    username
    first_name
    last_name
    email
    password
    groups
    user_permissions
    is_staff
    is_active
    is_superuser
    last_login
    date_joined
  For more information, go to: 
  https://docs.djangoproject.com/en/1.8/ref/contrib/auth/
  """
  user = models.OneToOneField(User)
  # Real first name, use first_name as preferred first name so we don't 
  # have to join on tables when fetching by name.
  real_name = models.CharField(max_length=200, blank=True)
  # e.g. 2012  
  class_year = models.CharField(max_length=4, blank=True)
  # e.g. 2021135727
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
