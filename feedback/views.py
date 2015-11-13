from tempfile import NamedTemporaryFile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from core.util import normalize_name

from rolepermissions.decorators import has_role_decorator
from xlwt import Workbook

from forms import ApplicantForm, FeedbackForm
from models import Applicant, Feedback
from templatetags import feedback_tags

# Create your views here.
@login_required
def index(request):
  applicants = Applicant.objects.all().order_by('first_name')
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/index.html', context)

@login_required
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

@login_required
@has_role_decorator('staff')
def export(request):
  applicants = Applicant.objects.all().order_by('last_name')
  book = Workbook()
  sheet1 = book.add_sheet('Rating Averages')
  sheet2 = book.add_sheet('Ratings');
  sheet1.write(0, 0, 'Applicant')
  sheet1.write(0, 1, 'Rating Average')
  sheet1.write(0, 2, 'Interest Average')
  sheet1.write(0, 3, 'Feedback Count')
  sheet2.write(0, 0, 'Applicant')
  sheet2.write(0, 1, 'Commenter')
  sheet2.write(0, 2, 'Rating')
  sheet2.write(0, 3, 'Interest')
  sheet2.write(0, 4, 'Comment')

  #Keep track of the line in the second sheet.
  s2_line = 1

  for i, applicant in enumerate(applicants):
    #Get all the feedback on an applicant ordered by descending rating
    feedbacks = Feedback.objects.filter(applicant=applicant).order_by('-rating')

    sheet1.write(i+1, 0, '%s, %s' % (applicant.last_name, applicant.first_name))
    sheet1.write(i+1, 1, feedback_tags.rating_average(feedbacks, num=True))
    sheet1.write(i+1, 2, feedback_tags.interest_average(feedbacks, num=True))
    sheet1.write(i+1, 3, int(feedback_tags.feedback_count(feedbacks)))

    for feedback in feedbacks:
      commenter = feedback.scholar
      if feedback.rating or feedback.interest or feedback.comments:
        sheet2.write(s2_line, 0, '%s, %s' % (applicant.last_name, applicant.first_name))
        sheet2.write(s2_line, 1, commenter.get_full_name())
        if feedback.rating:
          sheet2.write(s2_line, 2, feedback.rating)
        if feedback.interest:
          sheet2.write(s2_line, 3, feedback.interest)
        sheet2.write(s2_line, 4, feedback.comments)
      s2_line += 1

  with NamedTemporaryFile() as f:
    book.save(f)
    f.seek(0)
    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sneak_peek_2015.xls"'
    return response
