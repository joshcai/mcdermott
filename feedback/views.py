from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from core.util import normalize_name

from rolepermissions.decorators import has_role_decorator

from forms import ApplicantForm, FeedbackForm
from models import Applicant, Feedback

# Create your views here.
@login_required
def index(request):
  applicants = Applicant.objects.all().order_by('first_name')
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/index.html', context)

@login_required
@has_role_decorator('staff')
def applicant_table(request):
  applicants = Applicant.objects.all().order_by('first_name')
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/applicant_table.html', context)

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
  if request.method == 'POST':
    form = FeedbackForm(request.POST, instance=feedback)
    if (form.is_valid()):
      form.save()
      return redirect('feedback:index')
  else:
    form = FeedbackForm(instance=feedback)
  all_feedback = Feedback.objects.filter(applicant=applicant)
  context = {
      'feedback': all_feedback,
      'applicant': applicant,
      'form': form,
      }
  return render(request, 'feedback/applicant.html', context)

@login_required
def edit_applicant(request, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name))
  except Applicant.DoesNotExist:
    raise Http404('Applicant does not exist.')
  if request.method == 'POST':
    form = ApplicantForm(request.POST, request.FILES, instance=applicant)
    if (form.is_valid()):
      form.save()
      return redirect('feedback:applicant_profile', applicant.norm_name)
  else:
    form = ApplicantForm(instance=applicant)
  context = {
      'applicant': applicant,
      'form': form,
      }
  return render(request, 'feedback/edit_applicant.html', context)

@login_required
def add_applicant(request):
  applicant = Applicant()
  if request.method == 'POST':
    form = ApplicantForm(request.POST, request.FILES, instance=applicant)
    if (form.is_valid()):
      form.save()
      return redirect('feedback:applicant_profile', applicant.norm_name)
  else:
    form = ApplicantForm(instance=applicant)
  context = {
      'form': form,
  }
  return render(request, 'feedback/add_applicant.html', context)
