from django import forms

from models import McUser

class McUserForm(forms.ModelForm):
  class Meta:
    model = McUser
    fields = [
        'first_name',
        'real_name',
        'last_name',
        'gender',
        'class_year',
        'utd_id',
        'major',
        'major2',
        'minor',
        'minor2',
        'hometown',
        'high_school',
        'phone_number',
        'id',
        'pic'
    ]
    widgets = {'id': forms.HiddenInput()}

class UploadFileForm(forms.Form):
  file = forms.FileField()
