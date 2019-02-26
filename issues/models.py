from django.db import models

from core.models import McUser

# Create your models here.

class Issue(models.Model):
  title = models.CharField(max_length=50)
  body = models.TextField(max_length=200)

class Suggestion(models.Model):
  submitter = models.ForeignKey(McUser, blank=True)
  title = models.CharField(max_length=50)
  body = models.TextField(max_length=200)
