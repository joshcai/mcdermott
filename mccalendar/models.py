from django.db import models
from core.models import McUser

class McEvent(models.Model):
    mcevent_next_id = 1
    """Calendar event model
    """
    #needed for Google Calendar export
    owner = models.OneToOneField(McUser)
    subject = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    all_day_event = models.BooleanField()
    description = models.TextField(max_length=200, blank=True)
    location = models.TextField(max_length=200, blank=True)
    private = models.BooleanField()

    #additional fields
    #relevant_years = models.IntegerField(default=2015)

class McClass(models.Model):
    """Class model needed for ManyToMany relationship
    """
    year = models.IntegerField()
