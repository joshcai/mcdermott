import floppyforms as forms

from models import McUser

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
    widgets = {
        'id': forms.HiddenInput(),
        'pic': ImageThumbnailInput
    }

class UploadFileForm(forms.Form):
  file = forms.FileField()
