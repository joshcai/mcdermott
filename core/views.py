from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
import watson

from forms import McUserForm, DegreeForm
from models import McUser, Degree, Experience
from serializers import UserSerializer
from util import normalize_name

DegreeFormSet = modelformset_factory(Degree, form=DegreeForm, extra=1, can_delete=True)

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
  degrees = Degree.objects.filter(user_id=user_info.id)
  if request.method == 'POST':
    degrees_formset = DegreeFormSet(request.POST, queryset=degrees, initial=[{'user': user_info.id}])
    print dir(degrees_formset)
    if (degrees_formset.is_valid()):
      degrees_formset.save()
      return redirect('edit_edu')
  else:
    degrees_formset = DegreeFormSet(queryset=degrees, initial=[{'user': user_info.id}])
  context = {
      'degrees_formset': degrees_formset,
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
