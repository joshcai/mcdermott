from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rolepermissions.verifications import has_role, has_permission
import watson

from forms import McUserForm, DegreeForm, ExperienceForm, StudyAbroadForm
from models import McUser, Degree, Experience, StudyAbroad
from serializers import UserSerializer
from util import normalize_name

DegreeFormSet = modelformset_factory(Degree, form=DegreeForm, extra=1, can_delete=True)
ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)
StudyAbroadFormSet = modelformset_factory(StudyAbroad, form=StudyAbroadForm, extra=1, can_delete=True)

# Create your views here.
def index(request):
  return render(request, 'core/index.html')

@login_required
def edit_info(request, name):
  user_info = McUser.objects.get(norm_name=normalize_name(name))
  if not user_info.user.id == request.user.id and not has_permission(request.user, 'edit_all_info'):
    return redirect('edit_info', request.user.mcuser.norm_name)
  if request.method == 'POST':
    form = McUserForm(request.POST, request.FILES, instance=user_info, prefix='base')
    if (form.is_valid()):
      mcuser = form.save(commit=False)
      hidden_fields = [key.replace('checkbox_', '') for key in request.POST if key.startswith('checkbox_')]
      mcuser.hidden_fields = hidden_fields
      mcuser.save()
      messages.add_message(request, messages.SUCCESS, 'Changes saved!')
      return redirect('edit_info', user_info.norm_name)
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
      messages.add_message(request, messages.SUCCESS, 'Changes saved!')
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
      messages.add_message(request, messages.SUCCESS, 'Changes saved!')
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
      messages.add_message(request, messages.SUCCESS, 'Changes saved!')
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
  scholars = McUser.objects.all().order_by('first_name')
  context = {
    'scholars': scholars,
    'active': 'all'
    }
  return render(request, 'core/scholars.html', context)

@login_required
def staff(request):
  scholars = McUser.objects.all().filter(user__groups__name='staff').order_by('staff_order')
  context = {
    'scholars': scholars,
    'active': 'staff'
    }
  return render(request, 'core/staff.html', context)

@login_required
def scholars_by_class(request, class_year):
  scholars = McUser.objects.all().filter(class_year=int(class_year)).order_by('first_name')
  context = {
    'scholars': scholars,
    'active': str(class_year)
    }
  return render(request, 'core/scholars.html', context)

def resolveurl(request, url):
  return redirect('/%s' % url)

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
  return render(request, 'core/scholars.html', context)

@login_required
def profile(request, name):
  name = normalize_name(name)
  # TODO(joshcai): handle case where more than 1 user (aka users have same name)
  try:
    profile = McUser.objects.get(norm_name=name)
  except McUser.DoesNotExist:
    raise Http404('Page does not exist')
  # 'user' is already passed in as default (the logged in user),
  # so use 'profile' as alias
  context = {
      'profile': profile,
      'is_self': profile == request.user.mcuser
    }
  return render(request, 'core/profile.html', context)

@login_required
def documents(request):
  return render(request, 'core/documents.html')


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
