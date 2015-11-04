from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from core.util import normalize_name

from forms import ApplicantForm, FeedbackForm
from models import Applicant, Feedback

# Create your views here.
@login_required
def index(request):
  applicants = Applicant.objects.all()
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/index.html', context)

@login_required
def applicant_profile(request, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name))
  except Applicant.DoesNotExist:
    raise Http404('Applicant does not exist.')
  try:
    feedback = Feedback.objects.get(applicant=applicant, scholar=request.user.mcuser)
  except Feedback.DoesNotExist:
    feedback = Feedback()
    feedback.applicant = applicant
    feedback.scholar = request.user.mcuser
    feedback.save()
  if request.method == 'POST':
    form = FeedbackForm(request.POST, instance=feedback)
    if (form.is_valid()):
      form.save()
      return redirect('feedback:index')
  else:
    form = FeedbackForm(instance=feedback)
  context = {
      'applicant': applicant,
      'form': form,
      }
  return render(request, 'feedback/applicant.html', context)

@login_required
def edit_applicant(request, name):
  pass

@login_required
def add_applicant(request):
  pass
