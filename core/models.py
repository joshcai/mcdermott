from django.contrib.auth.models import User
from django.db import models
import watson
from sorl.thumbnail import ImageField

from util import normalize_name

from majors import MAJOR_CHOICES
from minors import MINOR_CHOICES

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

  # Gender
  MALE = 'Male'
  FEMALE = 'Female'
  GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=MALE, blank=False)

  # e.g. 2012
  YEARS = (
  (2000, '2000'), (2001, '2001'), (2002, '2002'), (2003, '2003'), (2004, '2004'), (2005, '2005'),
  (2006, '2006'), (2007, '2007'), (2008, '2008'), (2009, '2009'), (2010, '2010'), (2011, '2011'),
  (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015')
  )

  class_year = models.IntegerField(choices=YEARS, blank=True)

  # e.g. 2021135727
  utd_id = models.CharField(max_length=50, blank=True)

  # Fields of study
  major = models.CharField(max_length=200, choices=MAJOR_CHOICES, blank=True)
  major2 = models.CharField(max_length=200, choices=MAJOR_CHOICES, blank=True)
  MINOR_CHOICES = sorted(MINOR_CHOICES, key=lambda major:major[0]) #Remove when scraper is finished
  minor = models.CharField(max_length=200, choices=MINOR_CHOICES, blank=True)
  minor2 = models.CharField(max_length=200, choices=MINOR_CHOICES, blank=True)

  # Personal info
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
