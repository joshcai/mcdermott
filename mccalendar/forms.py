import floppyforms as forms
from functools import partial

from models import McEvent

DateInput = partial(forms.TextInput, {'class': 'datepicker'})
TimeInput = partial(forms.TextInput, {'class': 'timepicker'})

class McEventForm(forms.ModelForm):
  class Meta:
    model = McEvent
    fields = [
    #   'owner',
      'id',
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
      'description': forms.Textarea(attrs={'rows':4}),
    }

class UploadFileForm(forms.Form):
  file = forms.FileField()
