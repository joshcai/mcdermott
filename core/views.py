from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import viewsets
import watson

from forms import McUserForm
from models import McUser
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
    form = McUserForm(request.POST, request.FILES, instance=user_info)
    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = McUserForm(instance=user_info)
  context = {
      'form': form
      }
  return render(request, 'core/edit_info.html', context)

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
    scholars.extend([r.object for r in results])
  context = {
    'scholars': scholars
    }
  return render(request, 'core/scholars.html', context)

# TODO(joshcai): return another function, wrapped with login_required.
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
      'profile': profile
    }
  return render(request, 'core/profile.html', context)


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
