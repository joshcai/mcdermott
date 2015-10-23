from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rolepermissions.decorators import has_role_decorator

from models import Document
from forms import DocumentForm
import re

# Create your views here.

def index(request):
  return redirect(reverse('documents:view_docs', args=['meeting']))

def view_docs(request, category):
  documents = Document.objects.filter(category=category)
  choices = [c[1] for c in Document._meta.get_field('category').choices[1:]]

  context = {
    'documents': documents,
    'choices': choices,
  }
  return render(request, 'documents/view_docs.html', context)

@login_required
# @has_role_decorator('staff')
def create_doc(request):
  if request.method == 'POST':
    doc = Document()
    form = DocumentForm(request.POST, request.FILES, instance=doc)
    if (form.is_valid()):
      form.save()
      return redirect(reverse('documents:index'))
    else:
      form = DocumentForm(request.POST, request.FILES, instance=doc)
  else:
    form = DocumentForm()
  context = {
    'form':form,
    'form_url':reverse('documents:create_doc'),
  }
  return render(request, 'documents/edit_doc.html', context)

@login_required
# @has_role_decorator('staff')
def edit_doc(request, doc_id=None):
  try:
    doc = Document.objects.get(id=doc_id)
  except Document.DoesNotExist:
    return redirect('documents:create_event')
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES, instance=doc)
    if (form.is_valid()):
      form.save()
      return redirect(reverse('documents:index'))
    else:
      form = DocumentForm(request.POST, request.FILES, instance=event)
  else:
    form = DocumentForm(instance=doc)
  context = {
    'form':form,
    'form_url': reverse('documents:edit_doc', args=[doc_id])
  }
  return render(request, 'documents/edit_doc.html', context)
