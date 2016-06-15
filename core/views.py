from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rolepermissions.verifications import has_role, has_permission
from rolepermissions.decorators import has_role_decorator
import watson

import time
import requests

from forms import McUserForm, McUserStaffForm, DegreeForm, ExperienceForm, StudyAbroadForm, UserForm, HonorForm
from models import McUser, Degree, Experience, StudyAbroad, Honor
from serializers import UserSerializer
from util import normalize_name

try:
  from mcdermott.config import GA_TRACKING_ID
except ImportError:
  from mcdermott.example_config import GA_TRACKING_ID

DegreeFormSet = modelformset_factory(Degree, form=DegreeForm, extra=1, can_delete=True)
ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)
StudyAbroadFormSet = modelformset_factory(StudyAbroad, form=StudyAbroadForm, extra=1, can_delete=True)
HonorFormSet = modelformset_factory(Honor, form=HonorForm, extra=1, can_delete=True)

# Create your views here.
def index(request):
  if request.user.is_authenticated() and not request.user.mcuser.activated:
    request.user.mcuser.activated = True
    request.user.mcuser.save()
  context = {
    'ga_tracking_id': GA_TRACKING_ID
  }
  return render(request, 'core/index.html', context)
  
def update_last_updated(user):
  # updates the updated_alumni_info field with current date
  date_str = time.strftime('%m/%d/%Y')
  user.updated_alumni_info = date_str
  user.save()

@login_required
def edit_info(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_info', request.user.mcuser.norm_name)
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[mcuser.norm_name]))
      update_last_updated(user_info)
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.norm_name]))
      update_last_updated(user_info)
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.norm_name]))
      update_last_updated(user_info)
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.norm_name]))
      update_last_updated(user_info)
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.norm_name]))
      update_last_updated(user_info)
      return redirect('edit_honor', user_info.norm_name)
  else:
    honor_formset = HonorFormSet(queryset=honor, initial=[{'user': user_info.id}])
  context = {
      'honor_formset': honor_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_honor.html', context)
  
@login_required
def edit_account(request):
  user = request.user
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=user)
    if (user_form.is_valid()):
      user_form.save()
      messages.add_message(
        request, messages.SUCCESS,
        'Changes saved!')
      return redirect('edit_account')
  else:
    user_form = UserForm(instance=user)
  context = {
      'form': user_form
      }
  return render(request, 'core/edit_account.html', context)

def sign_up(request):
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
        'Changes saved! Click <a href="%s">here</a> to view profile.' % reverse('profile', args=[user_info.norm_name]))
      return redirect('edit_abroad', user_info.norm_name)
  else:
    study_abroad_formset = StudyAbroadFormSet(queryset=study_abroad, initial=[{'user': user_info.id}])
  context = {
      'study_abroad_formset': study_abroad_formset,
      'mcuser': user_info
      }
  return render(request, 'core/edit_abroad.html', context)

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
    return redirect('profile', scholars[0].norm_name)
  return render(request, 'core/scholars.html', context)

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

@login_required
def documents(request):
  return render(request, 'core/documents.html')


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
