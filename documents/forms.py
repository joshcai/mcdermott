import floppyforms as forms
from models import Document

class DocumentForm(forms.ModelForm):
  class Meta:
    model = Document
    fields = [
     'name',
     'category',
     'description',
     'actual_file',
    ]
