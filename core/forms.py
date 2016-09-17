from django.contrib.auth.models import User

import floppyforms as forms
from functools import partial

from django.core.exceptions import ValidationError
from models import McUser, Degree, Experience, StudyAbroad, Honor

DateInput = partial(forms.TextInput, {'class': 'datepicker'})

class ImageThumbnailInput(forms.ClearableFileInput):
  template_name = 'floppyforms/image_thumbnail.html'

class McUserForm(forms.ModelForm):
  class Meta:
    model = McUser
    fields = [
        'title',
        'first_name',
        'real_name',
        'last_name',
        'maiden_name',
        'birthday',
        'gender',
        'class_year',
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
        'mailing_address_type',
        'in_dfw',
        'current_city',
        'significant_other',
        'children',
        'personal_news',
    ]
    widgets = {
        'id': forms.HiddenInput(),
        'pic': ImageThumbnailInput,
        'birthday': DateInput(),
        'mailing_address_type': forms.Select(
            choices=(('', ''),
                     ('parent', 'parent address'),
                     ('alum', 'current alum address'))),
        'in_dfw': forms.Select(
            choices=(('', ''),
                     ('Yes', 'Yes'),
                     ('No', 'No'))),
        'personal_news': forms.Textarea(attrs={'rows':4, 'cols':15}),
    }


class McUserStaffForm(forms.ModelForm):
  class Meta:
    model = McUser
    fields = [
        'title',
        'first_name',
        'real_name',
        'last_name',
        'maiden_name',
        'birthday',
        'gender',
        'class_year',
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
        'mailing_address_type',
        'married',
        'in_dfw',
        'current_city',
        'right_after',
        'ultimate',
        'significant_other',
        'children',
        'personal_news',
        'num_degrees'
    ]
    widgets = {
        'id': forms.HiddenInput(),
        'pic': ImageThumbnailInput,
        'birthday': DateInput(),
        'mailing_address_type': forms.Select(
            choices=(('', ''),
                     ('parent', 'parent address'),
                     ('alum', 'current alum address'))),
        'right_after': forms.Select(
            choices=(('', ''),
                     ('grad', 'grad'),
                     ('employment', 'employment'),
                     ('prof', 'prof'))),
        'in_dfw': forms.Select(
            choices=(('', ''),
                     ('Yes', 'Yes'),
                     ('No', 'No'))),
        'ultimate': forms.Select(
            choices=(('', ''),
                     ('grad', 'grad'),
                     ('prof', 'prof'))),
        'personal_news': forms.Textarea(attrs={'rows':4, 'cols':15}),
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
      'major1': forms.TextInput(),
      'major2': forms.TextInput(),
      'minor1': forms.TextInput(),
      'minor2': forms.TextInput(),
      'start_time': DateInput(),
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
  new_password = forms.CharField(widget=forms.PasswordInput())
  new_password_confirm = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = [
      'username',
      'email',
    ]

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user', None)
    super(UserForm, self).__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    new_password = cleaned_data.get('new_password')
    new_password_confirm = cleaned_data.get('new_password_confirm')

    if new_password != new_password_confirm:
      raise ValidationError('Password fields did not match.')

  def save(self, commit=True):
    self.user.set_password(self.cleaned_data['new_password'])
    return super(UserForm, self).save(commit=commit)
