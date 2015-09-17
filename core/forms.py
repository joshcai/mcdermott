import floppyforms as forms

from models import McUser, Degree, Experience

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
      'user': forms.HiddenInput()
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
      'description': forms.Textarea(attrs={'rows':4, 'cols':15})
    }
