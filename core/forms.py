from django.forms import ModelForm, HiddenInput

from models import UserInfo

class UserInfoForm(ModelForm):
  class Meta:
    model = UserInfo
    fields = ['utd_id', 'major', 'major2', 'minor', 'minor2', 'hometown',
              'high_school', 'phone_number', 'user']
    widgets = {'user': HiddenInput()}