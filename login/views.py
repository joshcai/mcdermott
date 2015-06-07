from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def login(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      # Redirect to a success page.
    else:
      # Return a 'disabled account' error message
      pass
  else:
    # Return an 'invalid login' error message.
    pass


def logout(request):
    logout(request)