from django import forms

from models import McEvent

class McEventForm(forms.ModelForm):
  class Meta:
    model = McEvent
    fields = [
    #   'owner',
      'subject',
      'start_date',
      'start_time',
      'end_date',
      'end_time',
      'all_day_event',
      'description',
      'location',
      'private',
      #'relevant_years',
    ]
    widgets = {'id': forms.HiddenInput()}

class UploadFileForm(forms.Form):
  file = forms.FileField()
