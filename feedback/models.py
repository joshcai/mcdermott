from django.db import models
from localflavor.us.us_states import US_STATES
from sorl.thumbnail import ImageField

from core.models import McUser
from core.util import normalize_name

class Event(models.Model):
  full_name = models.CharField(max_length=200, blank=True)
  name = models.CharField(max_length=200, blank=True) # short name of event

# Create your models here.
class Applicant(models.Model):
  """Model for an applicant."""
  first_name = models.CharField(max_length=200, blank=True)
  last_name = models.CharField(max_length=200, blank=True)
  norm_name = models.CharField(max_length=400, blank=True)
  hometown = models.CharField(max_length=200, blank=True)
  hometown_state = models.CharField(blank=True, max_length=2, choices=US_STATES)
  high_school = models.CharField(max_length=200, blank=True)

  event = models.ForeignKey(Event, null=True, blank=True, default=None)

  attended = models.BooleanField(blank=False, null=False, default=True)

  GENDER_CHOICES = (('', ''), ('Mr.', 'Male'), ('Ms.', 'Female'))
  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)

  pic = ImageField(upload_to='applicants', blank=True)
  actual_pic = ImageField(upload_to='applicants_actual', blank=True)

  def get_full_name(self):
    return '%s %s' % (self.first_name, self.last_name)

  def save(self, *args, **kwargs):
    self.norm_name = normalize_name(self.get_full_name())
    super(Applicant, self).save(*args, **kwargs)

class Feedback(models.Model):
  """Model for feedback from one scholar on an applicant."""
  scholar = models.ForeignKey(McUser)
  applicant = models.ForeignKey(Applicant)

  RATING_CHOICES = (
      (5, 'Strong Yes'),
      (4, 'Yes - little or no reservations'),
      (3, 'Yes - some reservations'),
      (2, 'No - significant reservations'),
      (1, 'Strong No'),
      (0, 'Could not tell based on interaction'),
  )
  rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=False, default=None)

  INTEREST_CHOICES = (
      (5, 'Absolutely'),
      (4, 'Strongly interested - not ready to commit'),
      (3, 'Maybe'),
      (1, 'No'),
      (0, 'Could not tell based on interaction'),
  )
  interest = models.IntegerField(choices=INTEREST_CHOICES, null=True, blank=False, default=None)

  comments = models.TextField(blank=True)

class State(models.Model):
  STATE_CHOICES = (
    (1, 'Restrict Access'),
    (2, 'Open'),
    (3, 'Prevent Feedback Update')
  )
  current = models.IntegerField(choices=STATE_CHOICES, null=False, blank=False, default=2)
