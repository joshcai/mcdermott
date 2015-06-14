from django.contrib.auth.decorators import login_required
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
def profile(request, first_name, last_name):
  profile = McUser.objects.get(user__first_name=first_name, 
                               user__last_name=last_name)
  # 'user' is already passed in as default (the logged in user), 
  # so use 'profile' as alias 
  context = {
      'profile': profile
    }
  return render(request, 'core/profile.html', context)