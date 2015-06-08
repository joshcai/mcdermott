from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'core/index.html')

def edit_info(request):
	return render(request, 'core/edit_info.html')