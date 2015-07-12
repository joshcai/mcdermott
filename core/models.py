from django.contrib.auth.models import User
from django.db import models
import watson
from sorl.thumbnail import ImageField

from util import normalize_name

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
  first_name = models.CharField(max_length=200, blank=True)
  last_name = models.CharField(max_length=200, blank=True)
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
  pic = ImageField(upload_to='img', blank=True)
  # normalized name, e.g. joshcai
  norm_name = models.CharField(max_length=400, blank=True)
  #TODO: add address field
  #TODO: allow multiple phone
  #TODO: allow backup emails

  def get_full_name(self):
    return '%s %s' % (self.first_name, self.last_name)

  def save(self, *args, **kwargs):
    self.norm_name = normalize_name(self.get_full_name())
    super(McUser, self).save(*args, **kwargs)

watson.register(McUser)
# at bottom for circular dependency
import signals