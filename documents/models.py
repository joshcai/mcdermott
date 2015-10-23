from django.db import models

# Create your models here.

class Document(models.Model):
  name = models.CharField(max_length=200)
  category = models.CharField(max_length=30, blank=True,
    choices=(
      ('', ''),
      ('meeting', 'Meeting Minutes/Presentations'),
      ('scholar', 'Scholar Directory'),
      ('travel', 'Travel Home'),
      ('study', 'Study Abroad'),
      ('professional', 'Professional Development'),
      ('program', 'Program Documents'),
      ('semester', 'Semester Reports'),
    ))
  description = models.CharField(max_length=200)
  actual_file = models.FileField(upload_to='docs',)
