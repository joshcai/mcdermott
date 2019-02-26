import floppyforms as forms
from models import Issue, Suggestion


class IssueForm(forms.ModelForm):
  class Meta:
    model = Issue
    fields = [
      'title',
      'body'
    ]
    widgets = {
      'body': forms.Textarea(attrs={'rows':5})
    }

class SuggestionForm(forms.ModelForm):
  class Meta:
    model = Suggestion
    fields = [
      'title',
      'body'
    ]
    widgets = {
      'body': forms.Textarea(attrs={'rows':5})
    }
