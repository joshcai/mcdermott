from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

from forms import McUserForm
from models import McUser

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
    form = McUserForm(request.POST, instance=user_info)
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
  scholars = User.objects.all()
  context = {
    'scholars': scholars
    }
  return render(request, 'core/scholars.html', context)


def normalize_name(name):
  return ''.join([c.lower() for c in name if c.isalpha()])

@login_required
def own_profile(request):
  name = normalize_name(request.user.get_full_name())
  return redirect('/%s' % name)

@login_required
def profile(request, name):
  # TODO(joshcai): make this more efficient by caching or indexing all users
  users = McUser.objects.all()
  name = normalize_name(name)
  profile = None
  for user in users:
    if normalize_name(user.user.get_full_name()) == name:
      profile = user
      break
  # TODO(joshcai): handle case where more than 1 user (aka users have same name)
  if profile is None:
    raise Http404('Page does not exist')
  # 'user' is already passed in as default (the logged in user), 
  # so use 'profile' as alias 
  context = {
      'profile': profile
    }
  return render(request, 'core/profile.html', context)