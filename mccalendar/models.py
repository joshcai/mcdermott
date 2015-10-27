from django.db import models
from core.models import McUser
from django import forms

class McEvent(models.Model):
    """Calendar event model
    """
    #needed for Google Calendar export
    owner = models.ForeignKey(McUser)
    subject = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField()
    end_time = models.TimeField(null=True, blank=True)
    all_day_event = models.BooleanField()
    description = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    private = models.BooleanField()

    #additional fields
    #relevant_years = models.IntegerField(default=2015)

class McClass(models.Model):
    """Class model needed for ManyToMany relationship
    """
    year = models.IntegerField()
