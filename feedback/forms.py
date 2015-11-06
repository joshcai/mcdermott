import floppyforms as forms

from core.models import McUser
from models import Applicant, Feedback

class ImageThumbnailInput(forms.ClearableFileInput):
  template_name = 'floppyforms/image_thumbnail.html'

class RadioNoULInput(forms.RadioSelect):
  template_name = 'floppyforms/radio_no_ul.html'

class ApplicantForm(forms.ModelForm):
  class Meta:
    model = Applicant
    fields = [
        'first_name',
        'last_name',
        'gender',
        'hometown',
        'hometown_state',
        'high_school',
        'pic',
    ]
    widgets = {
        'pic': ImageThumbnailInput,
    }

class FeedbackForm(forms.ModelForm):
  class Meta:
    model = Feedback
    fields = [
      'rating',
      'interest',
      'comments',
    ]
    widgets = {
      'rating': RadioNoULInput,
      'interest': RadioNoULInput,
      'comments': forms.Textarea(attrs={'rows':4}),
    }