from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
import watson

from forms import McUserForm, DegreeForm
from models import McUser, Degree, Major, Minor, Experience
from serializers import UserSerializer
from util import normalize_name

# Create your views here.
def index(request):
  return render(request, 'core/index.html')

@login_required
def edit_info(request):
  try:
    user_info = McUser.objects.get(user_id=request.user.id)
  except McUser.DoesNotExist:
    user_info = McUser(user_id=request.user.id)
  if request.method == 'POST':
    form = McUserForm(request.POST, request.FILES, instance=user_info, prefix='base')
    if (form.is_valid()):
      form.save()
      return redirect('edit_info')
  else:
    form = McUserForm(instance=user_info, prefix='base')
  context = {
      'form': form,
      }
  return render(request, 'core/edit_info.html', context)

@login_required
def edit_edu(request):
  try:
    user_info = McUser.objects.get(user_id=request.user.id)
  except McUser.DoesNotExist:
    user_info = McUser(user_id=request.user.id)
  try:
    degree = Degree.objects.get(user_id=user_info.id)
  except Degree.DoesNotExist:
    degree = Degree(user_id=user_info.id)
  MajorFormSet = inlineformset_factory(Degree, Major,
                                       fields=('utd_major',),
                                       max_num=2, extra=2)
  MinorFormSet = inlineformset_factory(Degree, Minor,
                                       fields=('utd_minor',),
                                       max_num=2, extra=2)
  if request.method == 'POST':
    degree_form = DegreeForm(request.POST, instance=degree, prefix='degree')
    major_formset = MajorFormSet(request.POST, instance=degree)
    minor_formset = MinorFormSet(request.POST, instance=degree)
    if (degree_form.is_valid() and
        major_formset.is_valid() and
        minor_formset.is_valid()):
      degree_form.save()
      major_formset.save()
      minor_formset.save()
      return redirect('edit_edu')
  else:
    degree_form = DegreeForm(instance=degree, prefix='degree')
    major_formset = MajorFormSet(instance=degree)
    minor_formset = MinorFormSet(instance=degree)
  context = {
      'degree_form': degree_form,
      'major_formset': major_formset,
      'minor_formset': minor_formset
      }
  return render(request, 'core/edit_edu.html', context)

@login_required
def scholars(request):
  scholars = McUser.objects.all()
  context = {
    'scholars': scholars
    }
  return render(request, 'core/scholars.html', context)

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
      elif isinstance(result.object, Degree) or isinstance(result.object, Experience):
        if result.object.user not in scholars:
          scholars.append(result.object.user)
      elif isinstance(result.object, Major) or isinstance(result.object, Minor):
        if result.object.degree.user not in scholars:
          scholars.append(result.object.degree.user)
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
      'edit': profile == request.user.mcuser
    }
  return render(request, 'core/profile.html', context)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
