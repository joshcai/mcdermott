import floppyforms as forms

from models import McUser, Degree

class ImageThumbnailInput(forms.ClearableFileInput):
  template_name = 'floppyforms/image_thumbnail.html'

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
        'hometown',
        'high_school',
        'phone_number',
        'id',
        'pic'
    ]
    widgets = {
        'id': forms.HiddenInput(),
        'pic': ImageThumbnailInput
    }

class UploadFileForm(forms.Form):
  file = forms.FileField()

class DegreeForm(forms.ModelForm):
  class Meta:
    model = Degree
    fields = [
      'school',
      'degree_type',
      'start_time',
      'end_time'
    ]