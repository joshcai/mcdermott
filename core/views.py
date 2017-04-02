from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms.models import modelformset_factory
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rolepermissions.verifications import has_role, has_permission
from rolepermissions.decorators import has_role_decorator
import watson
import geocoder

from collections import defaultdict
import time
import requests
from tempfile import NamedTemporaryFile
from xlwt import Workbook

from forms import McUserForm, McUserStaffForm, DegreeForm, ExperienceForm, StudyAbroadForm, UserForm, HonorForm
from models import McUser, Degree, Experience, StudyAbroad, Honor, City
from serializers import UserSerializer
from util import normalize_name, log_slack

from feedback.views import get_latest_event

from mcdermott.config import GA_TRACKING_ID, GOOGLE_API_KEY

DegreeFormSet = modelformset_factory(Degree, form=DegreeForm, extra=1, can_delete=True)
ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)
StudyAbroadFormSet = modelformset_factory(StudyAbroad, form=StudyAbroadForm, extra=1, can_delete=True)
HonorFormSet = modelformset_factory(Honor, form=HonorForm, extra=1, can_delete=True)

# Create your views here.
def index(request):
  if request.user.is_authenticated() and not request.user.mcuser.activated:
    log_slack('User `%s` activated' % request.user.mcuser.get_full_name())
    request.user.mcuser.activated = True
    request.user.mcuser.save()
  context = {
    'ga_tracking_id': GA_TRACKING_ID,
    'latest_feedback_event': get_latest_event()
  }
  return render(request, 'core/index.html', context)
  
def update_last_updated(user, editor):
  # updates the updated_alumni_info field with current date
  date_str = time.strftime('%m/%d/%Y')
  user.updated_alumni_info = date_str
  user.last_edited_by = editor.username
  user.save()

@login_required
def edit_info(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_info', request.user.mcuser.get_link_name())
  if request.method == 'POST':
    if has_role(request.user, 'staff'):
      form = McUserStaffForm(request.POST, request.FILES, instance=user_info, prefix='base')
    else:
      form = McUserForm(request.POST, request.FILES, instance=user_info, prefix='base')
    if (form.is_valid()):
      mcuser = form.save(commit=False)
      hidden_fields = [key.replace('checkbox_', '') for key in request.POST if key.startswith('checkbox_')]
      mcuser.hidden_fields = hidden_fields
      mcuser.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[mcuser.get_link_name()]))
      update_last_updated(user_info, request.user)
      return redirect('edit_info', user_info.norm_name)
  else:
    if has_role(request.user, 'staff'):
      form = McUserStaffForm(instance=user_info, prefix='base')
    else:
      form = McUserForm(instance=user_info, prefix='base')
  context = {
      'form': form,
      'mcuser': user_info
      }
  template = 'core/edit_info.html'
  if has_role(user_info.user, 'staff'):
    template = 'core/edit_info_staff.html'
  return render(request, template, context)

@login_required
def edit_edu(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_edu', request.user.mcuser.norm_name)
  degrees = Degree.objects.filter(user_id=user_info.id)
  if request.method == 'POST':
    degrees_formset = DegreeFormSet(request.POST, queryset=degrees, initial=[{'user': user_info.id}])
    if (degrees_formset.is_valid()):
      degrees_formset.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.get_link_name()]))
      update_last_updated(user_info, request.user)
      return redirect('edit_edu', user_info.norm_name)
  else:
    degrees_formset = DegreeFormSet(queryset=degrees, initial=[{'user': user_info.id}])
  context = {
      'degrees_formset': degrees_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_edu.html', context)

@login_required
def edit_exp(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_exp', request.user.mcuser.norm_name)
  experiences = Experience.objects.filter(user_id=user_info.id)
  if request.method == 'POST':
    experiences_formset = ExperienceFormSet(request.POST, queryset=experiences, initial=[{'user': user_info.id}])
    if (experiences_formset.is_valid()):
      experiences_formset.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.get_link_name()]))
      update_last_updated(user_info, request.user)
      return redirect('edit_exp', user_info.norm_name)
  else:
    experiences_formset = ExperienceFormSet(queryset=experiences, initial=[{'user': user_info.id}])
  context = {
      'experiences_formset': experiences_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_exp.html', context)

@login_required
def edit_abroad(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_abroad', request.user.mcuser.norm_name)
  study_abroad = StudyAbroad.objects.filter(user_id=user_info.id)
  if request.method == 'POST':
    study_abroad_formset = StudyAbroadFormSet(request.POST, queryset=study_abroad, initial=[{'user': user_info.id}])
    if (study_abroad_formset.is_valid()):
      study_abroad_formset.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.get_link_name()]))
      update_last_updated(user_info, request.user)
      return redirect('edit_abroad', user_info.norm_name)
  else:
    study_abroad_formset = StudyAbroadFormSet(queryset=study_abroad, initial=[{'user': user_info.id}])
  context = {
      'study_abroad_formset': study_abroad_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_abroad.html', context)

@login_required
def edit_honor(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_honor', request.user.mcuser.norm_name)
  honor = Honor.objects.filter(user_id=user_info.id)
  if request.method == 'POST':
    honor_formset = HonorFormSet(request.POST, queryset=honor, initial=[{'user': user_info.id}])
    if (honor_formset.is_valid()):
      honor_formset.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.get_link_name()]))
      update_last_updated(user_info, request.user)
      return redirect('edit_honor', user_info.norm_name)
  else:
    honor_formset = HonorFormSet(queryset=honor, initial=[{'user': user_info.id}])
  context = {
      'honor_formset': honor_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_honor.html', context)
  
@login_required
def edit_account(request, name=None):
  if name and not has_role(request.user, ['staff', 'dev']):
    return redirect('edit_account')

  if name:
    user = McUser.objects.get(norm_name=normalize_name(name)).user
  else:
    user = request.user

  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=user, user=user)
    if user_form.is_valid():
      user_form.save()
      messages.add_message(request, messages.SUCCESS, 'Changes saved!')
      if name:
        return redirect('edit_other_account', name)
      return redirect('edit_account')
    else:
      messages.add_message(request, messages.WARNING, 'Passwords do not match.')
      user_form = UserForm(instance=user, user=user)
  else:
    user_form = UserForm(instance=user, user=user)
  context = {
    'form': user_form,
  }
  if name:
    context['name'] = user.mcuser.get_full_name()
  return render(request, 'core/edit_account.html', context)

@login_required
def scholars(request):
  if request.user.mcuser.class_year:
    return redirect('/scholars/class/%s' % request.user.mcuser.class_year)
  return redirect('/staff')

@login_required
def staff(request):
  scholars = McUser.objects.all().filter(user__groups__name='staff').order_by('staff_order')
  context = {
    'scholars': scholars,
    'active': 'staff',
    }
  return render(request, 'core/staff.html', context)

@login_required
def scholars_by_class(request, class_year):
  scholars = McUser.objects.all().filter(class_year=int(class_year)).order_by('first_name')
  context = {
    'scholars': scholars,
    'active': str(class_year),
    }
  return render(request, 'core/scholars.html', context)

def resolveurl(request, url):
  return redirect('/%s' % url)

@login_required
def married(request):
  scholars = McUser.objects.filter(married=True).order_by('last_name')
  context = {
    'scholars': scholars,
    'marriage_count': len(scholars) / 2
    }
  return render(request, 'core/married.html', context)
  
@login_required
def stats(request):
  married_scholars = McUser.objects.filter(married=True)
  all_scholars = McUser.objects.exclude(class_year__isnull=True)
  alumni = [scholar for scholar in all_scholars if scholar.is_alumni()]
  current = [scholar for scholar in all_scholars if not scholar.is_alumni()]
  num_degrees = all_scholars.aggregate(Sum('num_degrees'))
  context = {
    'marriage_count': len(married_scholars) / 2,
    'all_scholars_count': len(all_scholars),
    'num_degrees': num_degrees['num_degrees__sum'],
    'alumni_count': len(alumni),
    'current_count': len(current)
    }
  return render(request, 'core/stats.html', context)

@login_required
def own_profile(request):
  name = request.user.mcuser.norm_name
  return redirect('/%s' % name)

@login_required
def search(request):
  query = request.GET.get('q', '')
  scholars = []
  if query:
    results = watson.search(query)
    for result in results:
      if isinstance(result.object, McUser):
        if result.object not in scholars:
          scholars.append(result.object)
      elif (isinstance(result.object, Degree) or
            isinstance(result.object, Experience) or
            isinstance(result.object, StudyAbroad)):
        if result.object.user not in scholars:
          scholars.append(result.object.user)
  context = {
    'scholars': scholars
    }
  # go straight to scholar if only one result
  if len(scholars) == 1:
    return redirect('profile', scholars[0].get_link_name())
  return render(request, 'core/scholars.html', context)
  
def normalize_location(place):
  return ''.join([x.lower() for x in place if x.isalnum() or x == ' '])
  
def get_location_geocoded(city_norm, city_real):
  geo_real = '' # send this to geocoder if one of the special cases
  if city_norm == 'bay area':
    geo_real = 'San Franciso'
  elif city_norm == 'nola':
    geo_real = 'New Orleans'
  elif city_norm == 'socal':
    geo_real = 'Anaheim'
  city, created = City.objects.get_or_create(norm_name=city_norm)
  if not created:
    return (city.lat, city.lng)
  city.real_name = city_real
  g = geocoder.arcgis(geo_real or city_real)
  city.lat, city.lng = g.latlng
  city.save()
  return (city.lat, city.lng)

@login_required
def get_scholar_locations(request):
  all_scholars = McUser.objects.exclude(class_year__isnull=True)
  loc_users = {}
  loc_to_full_name = {}
  # We use this to dedupe cities with the same coordinates.
  geoloc_to_city = defaultdict(list)
  
  for user in sorted(all_scholars):
    if not user.current_city:
      continue

    location = normalize_location(user.current_city)
    if location not in loc_to_full_name:
      loc_to_full_name[location] = user.current_city
      loc_users[user.current_city] = {}
      geoloc = get_location_geocoded(location, user.current_city)
      loc_users[user.current_city]['location'] = geoloc
      loc_users[user.current_city]['scholars'] = []
      geoloc_to_city[geoloc].append(user.current_city)
    # This makes sure only one real city name gets used as key.
    loc_users[loc_to_full_name[location]]['scholars'].append(user.get_full_name_with_year())

  # This is needed to merge locations that have the same exact coordinates, since they will overlap in the map display.
  for cities in geoloc_to_city.values():
    if len(cities) <= 1:
      continue
    base_city = cities[0]
    for city in cities[1:]:
      loc_users[base_city]['scholars'].extend(loc_users[city]['scholars'])
      del loc_users[city]
    
  return JsonResponse(loc_users, safe=False)
    
def scholar_map(request):
  return render(request, 'core/map.html', {'google_api_key': GOOGLE_API_KEY})
  
@login_required
def profile(request, name):
  name = normalize_name(name)
  # TODO(joshcai): handle case where more than 1 user (aka users have same name)
  try:
    profile = McUser.objects.get(norm_name=name)
  except McUser.DoesNotExist:
    #TODO: check if URL with slash resolves then redirect to it
    if name in ('admin', 'calendar', 'documents', 'feedback', 'issues'):
      return redirect('%s/' % name)
    raise Http404('Page does not exist.')
  # 'user' is already passed in as default (the logged in user),
  # so use 'profile' as alias
  context = {
      'profile': profile,
      'is_self': profile == request.user.mcuser
    }
  return render(request, 'core/profile.html', context)

@has_role_decorator('dev')
def activated_users(request):
  scholars = McUser.objects.filter(activated=True).order_by('first_name')
  context = {
    'scholars': scholars,
    }
  return render(request, 'core/scholars.html', context)

@has_role_decorator('dev')
def unactivated_users(request):
  scholars = McUser.objects.filter(activated=False).order_by('first_name')
  context = {
    'scholars': scholars,
    }
  return render(request, 'core/scholars.html', context)

@has_role_decorator('dev')
def activate_users(request):
  users_sent = []
  if request.method == 'POST':
    unactivated_users = McUser.objects.filter(activated=False)
    for user in unactivated_users:
      if user.user.email:
        session = requests.session()
        url = request.build_absolute_uri(reverse('password_reset'))
        response = session.get(url)
        csrftoken = session.cookies['csrftoken']
        r = session.post(
          url,
          data={'email': user.user.email, 'csrfmiddlewaretoken': csrftoken},
          headers=dict(Referer=url))
        users_sent.append('%s - %s' % (user.get_full_name(), user.user.email))
  context = {
    'users_sent': users_sent,
    'unactivated': McUser.objects.filter(activated=False).count(),
    'activated': McUser.objects.filter(activated=True).count(),
  }
  return render(request, 'core/activate_users.html', context)

def get_field(degree):
  if not degree.major2 and not degree.minor1 and not degree.minor2:
    return degree.major1
  majors = []
  if degree.major1:
    majors.append(degree.major1)
  if degree.major2:
    majors.append(degree.major2)
  minors = []
  if degree.minor1:
    minors.append(degree.minor1)
  if degree.minor2:
    minors.append(degree.minor2)
  if not minors:
    return ', '.join(majors)
  majors = 'Major: %s' % ', '.join(majors)
  minors = 'Minor: %s' % ', '.join(minors)
  return '%s; %s' % (majors, minors)
  
@has_role_decorator(['staff', 'dev'])
def export_scholars(request, kind):
  all_scholars = McUser.objects.exclude(class_year__isnull=True).order_by('last_name')
  if kind == 'alumni':
    scholars = [scholar for scholar in all_scholars if scholar.is_alumni()]
  elif kind == 'current':
    scholars = [scholar for scholar in all_scholars if not scholar.is_alumni()]
  elif kind == 'all':
    scholars = all_scholars
  else:
    raise Http404('Page does not exist.')
  max_degrees = 0
  for scholar in scholars:
    if scholar.degrees.count() > max_degrees:
      max_degrees = scholar.degrees.count()
  book = Workbook()
  sheet1 = book.add_sheet('Scholars (%s)' % kind)
  sheet1_headings = ['Class', 'Title', 'First', 'Last', 'Married Name', 'McD Marriage', 'Right after McD', 'Ultimately grad/prof?',
                     '# Grad degrees (completed+in-progress)']
  for i in xrange(max_degrees):
    sheet1_headings.extend(['School #%d' % (i+1), 'Field #%d' % (i+1), 'Degree #%d' % (i+1)])
  sheet1_headings.extend(['Employment', 'Last updated', 'Address', 'City', 'State', 'Zip', 'Country', 'Parent or alum address',
                          'Email', 'Phone', 'Website', 'Currently in DFW Area?', 'Current City', 'Significant Other',
                          'Child(ren)', 'Personal news to share with the staff'])
  for i, heading in enumerate(sheet1_headings):
    sheet1.write(0, i, heading)
  
  for i, scholar in enumerate(scholars):
    sheet1_fields = [
      scholar.class_year,
      scholar.title,
      scholar.first_name,
      scholar.maiden_name if scholar.maiden_name else scholar.last_name,
      scholar.last_name if scholar.maiden_name else '',
      0.5 if scholar.married else None,
      scholar.right_after,
      scholar.ultimate,
      scholar.num_degrees,
      ]
    for degree in scholar.degrees.all():
      sheet1_fields.extend([degree.school, get_field(degree), degree.degree_type])
    # extend for scholars who don't have max num of degrees
    sheet1_fields.extend([''] * 3 * (max_degrees - scholar.degrees.count()))
    exps = []
    for exp in scholar.experiences.all():
      e = exp.organization
      if exp.location:
        e += ' (%s)' % exp.location
      exps.append(e)
    sheet1_fields.append('; '.join(exps))
    sheet1_fields.extend([
      scholar.updated_alumni_info,
      scholar.mailing_address,
      scholar.mailing_city,
      scholar.mailing_state,
      scholar.mailing_zip,
      scholar.mailing_country,
      scholar.mailing_address_type,
      scholar.email,
      scholar.phone_number,
      scholar.website,
      scholar.in_dfw,
      scholar.current_city,
      scholar.significant_other,
      scholar.children,
      scholar.personal_news
    ])
    for j, field in enumerate(sheet1_fields):
      sheet1.write(i+1, j, field)
      
  with NamedTemporaryFile() as f:
    book.save(f)
    f.seek(0)
    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="scholars-%s.xls"' % kind
    return response

@login_required
@has_role_decorator(['staff', 'dev'])
def latest_edits(request):
  users = McUser.objects.order_by('-updated_alumni_info')
  context = {
    'users': users
  }
  return render(request, 'core/latest_edits.html', context)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
