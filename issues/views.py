from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from models import Issue, Suggestion
from forms import IssueForm, SuggestionForm

import requests
import json
from mcdermott import settings

# Create your views here.

def index(request):
  if request.POST:
    issue = Issue()
    form = IssueForm(request.POST, instance=issue)
    if (form.is_valid()):
      #send issue to GitHub
      title = form.cleaned_data.get('title')
      body = form.cleaned_data.get('body')
      url = 'https://api.github.com/repos/mcdermott-scholars/mcdermott/issues'
      auth = (settings.GITHUB_USERNAME, settings.GITHUB_PASSWORD)
      data = {'title': title, 'body': body}
      r = requests.post(url, auth=auth, data=json.dumps(data))
      messages.add_message(
        request,
        messages.SUCCESS if r.status_code==201 else messages.ERROR,
        'Issue submitted' if r.status_code==201 else 'Error submitting issue',
      )
      return redirect(reverse('core:index'))
    else:
      form = IssueForm(request.POST, instance=issue)
  else:
    form = IssueForm()
  context = {
    'form': form,
  }
  return render(request, 'issues/index.html', context)

@login_required
def suggestion(request):
  if request.POST:
    suggestion = Suggestion()
    form = SuggestionForm(request.POST, instance=suggestion)
    if (form.is_valid()):
      title = form.cleaned_data.get('title')
      body = form.cleaned_data.get('body')
      messages.add_message(
        request,
        messages.SUCCESS,
        'Suggestion submitted'
      )
      return redirect(reverse('core:index'))
    else:
      form = SuggestionForm(request.POST, instance=suggestion)
  else:
    form = SuggestionForm()
  context = {
    'form': form,
  }
  return render(request, 'issues/suggestion.html', context)