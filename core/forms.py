from django.forms import ModelForm, HiddenInput

from models import McUser

class McUserForm(ModelForm):
  class Meta:
    model = McUser
    fields = ['real_name', 'class_year',  'utd_id', 'major', 'major2', 'minor', 
              'minor2', 'hometown', 'high_school', 'phone_number', 'id']
    widgets = {'id': HiddenInput()}