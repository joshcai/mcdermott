from django.db import models
from localflavor.us.us_states import US_STATES
from sorl.thumbnail import ImageField

from core.models import McUser
from core.util import normalize_name

# Create your models here.
class Applicant(models.Model):
  """Model for an applicant."""
  first_name = models.CharField(max_length=200, blank=True)
  last_name = models.CharField(max_length=200, blank=True)
  norm_name = models.CharField(max_length=400, blank=True)
  hometown = models.CharField(max_length=200, blank=True)
  hometown_state = models.CharField(blank=True, max_length=2, choices=US_STATES)
  high_school = models.CharField(max_length=200, blank=True)

  GENDER_CHOICES = (('', ''), ('Male', 'Male'), ('Female', 'Female'))
  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)

  pic = ImageField(upload_to='applicants', blank=True)

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
      (5, '5: Strong Yes'),
      (4, '4: Yes - little or no reservations'),
      (3, '3: Yes - some reservations'),
      (2, '2: No - significant reservations'),
      (1, '1: Strong No'),
      ('', 'None'),
  )
  rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)

  INTEREST_CHOICES = (
      (4, '4: Very enthusiastic!'),
      (3, '3: Interested'),
      (2, '2: Not interested'),
      (1, '1: Could not tell based on interaction'),
      ('', 'None'),
  )
  interest = models.IntegerField(choices=INTEREST_CHOICES, null=True, blank=True)

  comments = models.TextField(blank=True)
