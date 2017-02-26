from functools import wraps
from tempfile import NamedTemporaryFile

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from core.util import normalize_name, log_slack
from core.models import McUser

from rolepermissions.shortcuts import grant_permission, revoke_permission
from rolepermissions.verifications import has_role, has_permission
from rolepermissions.decorators import has_role_decorator
from xlwt import Workbook

from forms import ApplicantForm, FeedbackForm, StateForm, EventForm
from models import Applicant, Feedback, State, Event, Assignment, Favorite, Shortlist
from templatetags.feedback_tags import *

from mcdermott.roles import ApplicantEditor
from mcdermott.config import GA_TRACKING_ID

def restrict_access(f):
  @wraps(f)
  def wrapper(request, *args, **kwargs):

    if get_state().current == 1:
      if not (has_role(request.user, ['staff', 'dev', 'selection']) or has_permission(request.user, 'edit_applicants')):
        raise Http404('App not available until later.')
    return f(request, *args, **kwargs)
  return wrapper

# Create your views here.

# Returns the full name of the latest feedback event
def get_latest_event():
  try:
    event = Event.objects.latest('id').full_name
  except Event.DoesNotExist:
    return
  return event

@login_required
def events(request):
  events = Event.objects.order_by('-id')
  context = {
      'events': events
  }
  return render(request, 'feedback/events.html', context)

@login_required
@has_role_decorator(['staff', 'dev'])
def create_event(request):
  event = Event()
  if request.method == 'POST':
    form = EventForm(request.POST, instance=event)
    if (form.is_valid()):
      e = form.save(commit=False)
      if not Event.objects.filter(name=e.name).exists():
        e.save()
        return redirect('feedback:index', e.name)
      messages.add_message(request, messages.WARNING, 'Event with that short name already exists.')
  else:
    form = EventForm(instance=event)
  context = {
      'form': form,
  }
  return render(request, 'feedback/create_event.html', context)
  
@login_required
@has_role_decorator(['staff', 'dev'])
def edit_event(request, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    raise Http404('Event does not exist')
  if request.method == 'POST':
    form = EventForm(request.POST, instance=event)
    if (form.is_valid()):
      e = form.save(commit=False)
      events = Event.objects.filter(name=e.name)
      # To allow editing the same event and keeping its short name.
      alreadyExists = False
      for ev in events:
        if ev != event:
          alreadyExists = True
          break
      if not alreadyExists:
        e.save()
        return redirect('feedback:index', e.name)
      messages.add_message(request, messages.WARNING, 'Event with that short name already exists.')
  else:
    form = EventForm(instance=event)
  context = {
      'form': form,
      'event_name': event_name,
  }
  return render(request, 'feedback/edit_event.html', context)


@login_required
@restrict_access
def index_redirect(request):
  latest_event = Event.objects.latest('id')
  return redirect('feedback:index', latest_event.name)

@login_required
@restrict_access
def index(request, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    raise Http404('Event does not exist')
  applicants = Applicant.objects.filter(event__name=event_name).order_by('first_name')
  assignments = [x.applicant for x in Assignment.objects.filter(scholar=request.user.mcuser)]
  favorites = [x.applicant for x in Favorite.objects.filter(scholar=request.user.mcuser)]
  shortlist = [x.applicant for x in Shortlist.objects.filter(scholar=request.user.mcuser)]
  applicants = sorted(applicants, key=lambda a: a.get_full_name())
  context = {
    'assignments': assignments,
    'favorites': favorites,
    'shortlist': shortlist,
    'applicants': applicants,
    'event_name': event_name,
    'event': event,
    'ga_tracking_id': GA_TRACKING_ID
  }
  return render(request, 'feedback/index.html', context)

@login_required
@restrict_access
def applicant_table(request, event_name):
  applicants = Applicant.objects.filter(event__name=event_name).order_by('first_name')
  context = {
    'applicants': applicants,
    'event_name': event_name
  }
  return render(request, 'feedback/applicant_table.html', context)

@login_required
@restrict_access
def applicant_table_ratings(request, event_name):
  applicants = Applicant.objects.filter(event__name=event_name).order_by('first_name')
  context = {
    'applicants': applicants,
    'event_name': event_name
  }
  return render(request, 'feedback/applicant_table_ratings.html', context)

def favorited(scholar, applicant):
  return Favorite.objects.filter(applicant=applicant, scholar=scholar).exists()

@login_required
@restrict_access
def applicant_profile(request, event_name, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name), event__name=event_name)
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
    print 'got form'
    if (form.is_valid()):
      print 'form valid'
      form.save()
      if request.is_ajax():
        print 'returning json'
        return JsonResponse({'msg': 'saved successfully'})
      return redirect('feedback:index', event_name)
  else:
    form = FeedbackForm(instance=feedback)
  all_feedback = Feedback.objects.filter(applicant=applicant)

  context = {
      'feedback': all_feedback,
      'applicant': applicant,
      'form': form,
      'state': get_state(),
      'event_name': event_name,
      'favorited': favorited(request.user.mcuser, applicant)
      }
  return render(request, 'feedback/applicant.html', context)


@login_required
@csrf_exempt
def shortlist_applicant(request, event_name, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name), event__name=event_name)
  except Applicant.DoesNotExist:
    raise Http404('Applicant does not exist.')
  if request.method == 'POST':
    try:
      s = Shortlist.objects.get(applicant=applicant, scholar=request.user.mcuser)
      s.delete()
      return JsonResponse({'msg': 'unlisted'})
    except Shortlist.DoesNotExist:
      s = Shortlist(applicant=applicant, scholar=request.user.mcuser)
      s.save()
      return JsonResponse({'msg': 'listed'})
  return HttpResponse('Please POST')

@login_required
@csrf_exempt
def favorite_applicant(request, event_name, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name), event__name=event_name)
  except Applicant.DoesNotExist:
    raise Http404('Applicant does not exist.')
  if request.method == 'POST':
    try:
      fav = Favorite.objects.get(applicant=applicant, scholar=request.user.mcuser)
      fav.delete()
      return JsonResponse({'msg': 'unstarred'})
    except Favorite.DoesNotExist:
      favs = Favorite.objects.filter(scholar=request.user.mcuser)
      if favs.count() < 5:
        fav = Favorite(applicant=applicant, scholar=request.user.mcuser)
        fav.save()
        return JsonResponse({'msg': 'starred'})
      return JsonResponse({'msg': 'max stars given'})
  return HttpResponse('Please POST')

@login_required
def edit_applicant(request, event_name, name):
  try:
    applicant = Applicant.objects.get(norm_name=normalize_name(name), event__name=event_name)
  except Applicant.DoesNotExist:
    raise Http404('Applicant does not exist.')
  if request.method == 'POST':
    form = ApplicantForm(request.POST, request.FILES, instance=applicant)
    if (form.is_valid()):
      app = form.save(commit=False)
      app.save()
      log_slack('Applicant %s/%s edited by %s' % (name, app.get_full_name(), request.user.mcuser.get_full_name()))
      return redirect('feedback:applicant_profile', event_name, app.norm_name)
  else:
    form = ApplicantForm(instance=applicant)
  context = {
      'applicant': applicant,
      'form': form,
      'event_name': event_name
      }
  return render(request, 'feedback/edit_applicant.html', context)

@login_required
def add_applicant(request, event_name):
  applicant = Applicant()
  if request.method == 'POST':
    form = ApplicantForm(request.POST, request.FILES, instance=applicant)
    if (form.is_valid()):
      app = form.save(commit=False)
      if not Applicant.objects.filter(norm_name=app.norm_name).exists():
        event = Event.objects.get(name=event_name)
        app.event = event
        app.save()
        log_slack('Applicant %s added by %s' % (app.get_full_name(), request.user.mcuser.get_full_name()))
        return redirect('feedback:applicant_profile', event_name, applicant.norm_name)
  else:
    form = ApplicantForm(instance=applicant)
  context = {
      'form': form,
      'event_name': event_name
  }
  return render(request, 'feedback/add_applicant.html', context)

def get_state():
  try:
    state = State.objects.get()
  except State.DoesNotExist:
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
      return redirect('feedback:index_redirect')
  else:
    form = StateForm(instance=state)
  context = {
      'form': form,
      }
  return render(request, 'feedback/edit_state.html', context)

@login_required
def export(request, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    raise Http404('Event does not exist')
  if not request.user.mcuser in event.staff.all():
    raise Http404('Permission denied.')
  applicants = Applicant.objects.filter(event__name=event_name).order_by('last_name')
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
      rating_average(feedbacks, num=True),
      interest_average(feedbacks, num=True),
      int(feedback_count(feedbacks))
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
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % event.full_name
    return response

@login_required
def export_fw(request, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    raise Http404('Event does not exist')
  if not (request.user.mcuser in event.staff.all() or request.user.mcuser in event.selection.all()):
    raise Http404('Permission denied.') 
  applicants = Applicant.objects.filter(event__name=event_name).order_by('last_name')
  book = Workbook()
  sheet1 = book.add_sheet('Rating Averages')
  sheet2 = book.add_sheet('Ratings');
  sheet1_headings = ('Title', 'Last', 'First', 'High School', 'City', 'State', 'Attended',
                     'Rating - Alumni', 'Interest - Alumni', 'Favorite - Alumni', 'Feedback # - Alumni',
                     'Rating - Senior', 'Interest - Senior', 'Favorite - Senior', 'Feedback # - Senior',
                     'Rating - Other', 'Interest - Other', 'Favorite - Other', 'Feedback # - Other',
                     'Rating Average', 'Interest Average', 'Favorite Count', 'Feedback Count')
  for i, heading in enumerate(sheet1_headings):
    sheet1.write(0, i, heading)
  sheet2_headings = ('Last', 'First', 'Commenter', 'Rating', 'Interest', 'Comment')
  for i, heading in enumerate(sheet2_headings):
    sheet2.write(0, i, heading)

  #Keep track of the line in the second sheet.
  s2_line = 1

  for i, applicant in enumerate(applicants):
    #Get all the feedback on an applicant ordered by descending rating
    feedbacks_with_selection = Feedback.objects.filter(applicant=applicant).order_by('-rating')
    feedbacks = [f for f in feedbacks_with_selection if not f.scholar.selection]
    sheet1_fields = (
      applicant.gender,
      applicant.last_name,
      applicant.first_name,
      applicant.high_school,
      applicant.hometown,
      applicant.hometown_state,
      applicant.attended,
      rating_average(alumni_filter(feedbacks), num=True),
      interest_average(alumni_filter(feedbacks), num=True),
      len(alumni_filter(favorite_filter(applicant))),
      int(feedback_count(alumni_filter(feedbacks))),
      rating_average(senior_filter(feedbacks), num=True),
      interest_average(senior_filter(feedbacks), num=True),
      len(senior_filter(favorite_filter(applicant))),
      int(feedback_count(senior_filter(feedbacks))),
      rating_average(other_filter(feedbacks), num=True),
      interest_average(other_filter(feedbacks), num=True),
      len(other_filter(favorite_filter(applicant))),
      int(feedback_count(other_filter(feedbacks))),
      rating_average(feedbacks, num=True),
      interest_average(feedbacks, num=True),
      len(favorite_filter(applicant)),
      int(feedback_count(feedbacks))
      )
    for j, field in enumerate(sheet1_fields):
      sheet1.write(i+1, j, field)

    for feedback in feedbacks_with_selection:
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
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % event.full_name
    return response

