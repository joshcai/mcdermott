import floppyforms as forms
from models import Issue

class IssueForm(forms.ModelForm):
  class Meta:
    model = Issue
    fields = [
     'title',
     'body',
    ]
    widgets = {
      'body': forms.Textarea(attrs={'rows':5})
    }
