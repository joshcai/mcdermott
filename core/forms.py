from django.contrib.auth.models import User

import floppyforms as forms
from functools import partial

from models import McUser, Degree, Experience, StudyAbroad, Honor

DateInput = partial(forms.TextInput, {'class': 'datepicker'})

class ImageThumbnailInput(forms.ClearableFileInput):
  template_name = 'floppyforms/image_thumbnail.html'

class McUserForm(forms.ModelForm):
  class Meta:
    model = McUser
    fields = [
        'first_name',
        'real_name',
        'last_name',
        'birthday',
        'gender',
        'class_year',
        'utd_id',
        'hometown',
        'hometown_state',
        'high_school',
        'phone_number',
        'id',
        'pic',
        'staff_title',
        'staff_phone',
        'linkedin',
        'website',
        'facebook',
        'email',
        'dorm_type',
        'dorm_number',
        'mailing_address',
        'mailing_city',
        'mailing_state',
        'mailing_zip',
        'mailing_country',
        'in_dfw',
        'current_city',
    ]
    widgets = {
        'id': forms.HiddenInput(),
        'pic': ImageThumbnailInput,
        'birthday': DateInput(),
    }

class UploadFileForm(forms.Form):
  file = forms.FileField()

class DegreeForm(forms.ModelForm):
  class Meta:
    model = Degree
    fields = [
      'user',
      'school',
      'degree_type',
      'start_time',
      'end_time',
      'major1',
      'major2',
      'minor1',
      'minor2'
    ]
    widgets = {
      'user': forms.HiddenInput(),
      'start_time': DateInput(),
      'end_time': DateInput(),
    }

class ExperienceForm(forms.ModelForm):
  class Meta:
    model = Experience
    fields = [
      'user',
      'exp_type',
      'title',
      'organization',
      'description',
      'location',
      'start_time',
      'end_time'
    ]
    widgets = {
      'user': forms.HiddenInput(),
      'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
      'start_time': DateInput(),
      'end_time': DateInput(),

    }

class StudyAbroadForm(forms.ModelForm):
  class Meta:
    model = StudyAbroad
    fields = [
      'user',
      'study_abroad_type',
      'organization',
      'description',
      'primary_location',
      'other_locations',
      'start_time',
      'end_time'
    ]
    widgets = {
      'user': forms.HiddenInput(),
      'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
      'start_time': DateInput(),
      'end_time': DateInput(),
    }

class HonorForm(forms.ModelForm):
  class Meta:
    model = Honor
    fields = [
      'user',
      'title',
      'received_time'
    ]
    widgets = {
      'user': forms.HiddenInput(),
      'received_time': DateInput(),
    }
class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = [
      'username',
      'email',
    ]
