from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

from models import McEvent
from forms import McEventForm

# Create your views here.

#Default calendar view
@login_required
def index(request):
  events = McEvent.objects.all()
  context = {
    'events': events,
  }
  return render(request, 'mccalendar/index.html', context)

@login_required
def create_event(request):
  if request.method == 'POST':
    event = McEvent(owner=request.user.mcuser)
    form = McEventForm(request.POST, instance=event)
    if (form.is_valid()):
      form.save()
      return redirect('index')
    else:
      form = McEventForm(request.POST, instance=event)
  else:
    form = McEventForm()
  context = {
        'form':form,
  }
  return render(request, 'mccalendar/create_event.html', context)

@login_required
def event_detail(request, event_id):
  try:
    event = McEvent.objects.get(id=event_id)
  except McEvent.DoesNotExist:
    raise Http404('Event %s does not exist' %event_id)
  else:
    context = {
      'event':event
    }
    return render(request, 'mccalendar/event_detail.html', context)
