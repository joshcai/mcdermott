import floppyforms as forms
from functools import partial

from models import McEvent

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput = partial(forms.TimeInput, {'class': 'timepicker'})

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
    widgets = {
      'id': forms.HiddenInput(),
      'start_date': DateInput(),
      'start_time': TimeInput(),
      'end_date': DateInput(),
      'end_time': TimeInput(),
    }

class UploadFileForm(forms.Form):
  file = forms.FileField()
