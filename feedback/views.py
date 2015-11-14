from functools import wraps
from tempfile import NamedTemporaryFile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from core.util import normalize_name
from core.models import McUser

from rolepermissions.shortcuts import grant_permission, revoke_permission
from rolepermissions.verifications import has_role, has_permission
from rolepermissions.decorators import has_role_decorator
from xlwt import Workbook

from forms import ApplicantForm, FeedbackForm, StateForm
from models import Applicant, Feedback, State
from templatetags import feedback_tags

from mcdermott.roles import ApplicantEditor

def restrict_access(f):
  @wraps(f)
  def wrapper(request, *args, **kwargs):

    if get_state().current == 1:
      if not (has_role(request.user, 'staff') or has_permission(request.user, 'edit_applicants')):
        raise Http404('App not available until later.')
    return f(request, *args, **kwargs)
  return wrapper

# Create your views here.
@login_required
@restrict_access
def index(request):
  applicants = Applicant.objects.all().order_by('first_name')
  if not has_role(request.user, 'staff'):
    applicants = applicants.filter(attended=True)
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/index.html', context)

@login_required
@restrict_access
def applicant_table(request):
  applicants = Applicant.objects.all().order_by('first_name')
  if not has_role(request.user, 'staff'):
    applicants = applicants.filter(attended=True)
  context = {
    'applicants': applicants
  }
  return render(request, 'feedback/applicant_table.html', context)

@login_required
@restrict_access
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
      'state': get_state()
      }
  return render(request, 'feedback/applicant.html', context)

@login_required
def edit_applicant(request, name):
  if not (has_permission(request.user, 'edit_applicants') or
          has_role(request.user, ['staff', 'dev'])):
    raise Http404('Permission denied.')
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
  if not (has_permission(request.user, 'edit_applicants') or
          has_role(request.user, ['staff', 'dev'])):
    raise Http404('Permission denied.')
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
def grant_permission(request, scholar_name):
  if not has_role(request.user, ['staff', 'dev']):
    raise Http404('Permission denied.')
  try:
    mcuser = McUser.objects.get(norm_name=normalize_name(scholar_name))
    ApplicantEditor.assign_role_to_user(mcuser.user)
    grant_permission(mcuser.user, 'edit_applicants')
    return redirect('feedback:index')
  except McUser.DoesNotExist:
    raise Http404('User does not exist')

@login_required
def revoke_permission(request, scholar_name):
  if not has_role(request.user, ['staff', 'dev']):
    raise Http404('Permission denied.')
  try:
    mcuser = McUser.objects.get(norm_name=normalize_name(scholar_name))
  except McUser.DoesNotExist:
    raise Http404('User does not exist')
  revoke_permission(mcuser.user, 'edit_applicants')
  return redirect('feedback:index')

def get_state():
  try:
    state = State.objects.get()
  except State.DoestNotExist:
    state = State()
    state.save()
  return state

@login_required
def app_state(request):
  if not has_role(request.user, ['staff', 'dev']):
    raise Http404('Permission denied.')
  state = get_state()
  if request.method == 'POST':
    form = StateForm(request.POST, instance=state)
    if (form.is_valid()):
      form.save()
      return redirect('feedback:index')
  else:
    form = StateForm(instance=state)
  context = {
      'form': form,
      }
  return render(request, 'feedback/edit_state.html', context)

@login_required
@has_role_decorator('staff')
def export(request):
  applicants = Applicant.objects.all().order_by('last_name')
  book = Workbook()
  sheet1 = book.add_sheet('Rating Averages')
  sheet2 = book.add_sheet('Ratings');
  sheet1_headings = ('Title', 'Last', 'First', 'High School', 'City', 'State',
                     'Attended', 'Rating Average', 'Interest Average', 'Feedback Count')
  for i, heading in enumerate(sheet1_headings):
    sheet1.write(0, i, heading)
  sheet2_headings = ('Last', 'First', 'Commenter', 'Rating', 'Interest', 'Comment')
  for i, heading in enumerate(sheet2_headings):
    sheet2.write(0, i, heading)

  #Keep track of the line in the second sheet.
  s2_line = 1

  for i, applicant in enumerate(applicants):
    #Get all the feedback on an applicant ordered by descending rating
    feedbacks = Feedback.objects.filter(applicant=applicant).order_by('-rating')
    sheet1_fields = (
      applicant.gender,
      applicant.last_name,
      applicant.first_name,
      applicant.high_school,
      applicant.hometown,
      applicant.hometown_state,
      applicant.attended,
      feedback_tags.rating_average(feedbacks, num=True),
      feedback_tags.interest_average(feedbacks, num=True),
      int(feedback_tags.feedback_count(feedbacks))
      )
    for j, field in enumerate(sheet1_fields):
      sheet1.write(i+1, j, field)

    for feedback in feedbacks:
      commenter = feedback.scholar
      if feedback.rating or feedback.interest or feedback.comments:
        sheet2_fields = (
          applicant.last_name,
          applicant.first_name,
          '%s, %s' % (commenter.last_name, commenter.first_name),
          feedback.rating if feedback.rating else '',
          feedback.interest if feedback.interest else '',
          feedback.comments
          )
        for j, field in enumerate(sheet2_fields):
          sheet2.write(s2_line, j, field)
        s2_line += 1

  with NamedTemporaryFile() as f:
    book.save(f)
    f.seek(0)
    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sneak_peek_2015.xls"'
    return response
