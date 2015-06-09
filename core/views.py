from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms import UserInfoForm
from models import UserInfo

# Create your views here.
def index(request):
  return render(request, 'core/index.html')

@login_required
def edit_info(request):
  user_info = UserInfo.objects.get(user_id=request.user.id)
  if request.method == 'POST':
    form = UserInfoForm(request.POST, instance=user_info)
    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = UserInfoForm(instance=user_info)
  context = {
      'form': form
      }
  return render(request, 'core/edit_info.html', context)