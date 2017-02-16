from django.db import models
from localflavor.us.us_states import US_STATES
from sorl.thumbnail import ImageField

from core.models import McUser
from core.util import normalize_name

class Event(models.Model):
  full_name = models.CharField(max_length=200, blank=False)
  name = models.CharField(max_length=200, blank=False) # short name of event
  fw = models.BooleanField(blank=False, null=False, default=False)

# Create your models here.
class Applicant(models.Model):
  """Model for an applicant."""
  first_name = models.CharField(max_length=200, blank=False)
  last_name = models.CharField(max_length=200, blank=False)
  norm_name = models.CharField(max_length=400, blank=True)
  hometown = models.CharField(max_length=200, blank=True)
  hometown_state_long = models.CharField(max_length=200, blank=True)
  hometown_state = models.CharField(blank=True, max_length=2, choices=US_STATES)
  high_school = models.CharField(max_length=200, blank=True)
  major = models.CharField(max_length=200, blank=True)
  career = models.CharField(max_length=200, blank=True)
  group = models.CharField(max_length=200, blank=True)

  interviewers = models.ManyToManyField(McUser, related_name='interviewees')

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

class Assignment(models.Model):
  scholar = models.ForeignKey(McUser)
  applicant = models.ForeignKey(Applicant)

class Favorite(models.Model):
  scholar = models.ForeignKey(McUser)
  applicant = models.ForeignKey(Applicant)

class Shortlist(models.Model):
  scholar = models.ForeignKey(McUser)
  applicant = models.ForeignKey(Applicant)

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

  notes = models.TextField(blank=True)
  comments = models.TextField(blank=True)

class State(models.Model):
  STATE_CHOICES = (
    (1, 'Restrict Access'),
    (2, 'Open'),
    (3, 'Prevent Feedback Update')
  )
  current = models.IntegerField(choices=STATE_CHOICES, null=False, blank=False, default=2)

class InterviewFeedback(models.Model):
  """Model for feedback from one interviewer on an applicant."""
  interviewer = models.ForeignKey(McUser)
  applicant = models.ForeignKey(Applicant)