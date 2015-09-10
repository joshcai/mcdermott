from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

import time
import calendar

from models import McEvent
from forms import McEventForm

# Create your views here.

month_names = "January February March April May June July August September October November December".split()

#Default calendar view
@login_required
def index(request):
  cur_year, cur_month = time.localtime()[:2]
  events = McEvent.objects.all()
  context = {
    'events': events,
  }
  return redirect('/mccalendar/%s/%s/' % (cur_year, cur_month))

"""
@login_required
def year(request, year=None):
  cur_year, cur_month = time.localtime()[:2]

  #create list of months
  month_list = []
  for nm, month in enumerate(months):
    event = current = False
    events = McEvent.objects.filter(start_date__year=year, start_date__month=n+1)

    if events:
      event = True
    if year == cur_year and nm+1 == cur_month:  #enumerate starts at 0, but months at 1
      current = True  #to highlight the current month?
    month_list.append(dict(n=n+1, name=month, entry=entry, current=current))

  context = {
    'n':n,
    'months':month_list,
    'year':year,
  }
  return render(request, 'mccalendar/year.html', context)
"""

@login_required
def month(request, year=None, month=None, change=None):
  year = int(year) if year else time.localtime()[0]
  month = int(month) if month else time.localtime()[1]

  #apply next/previous if applicable
  if change in ('next', 'prev'):
    if change=='next':
      month = month+1
      if month == 13:
        month = 1
        year += 1
    elif change=='prev':
      month = month-1
      if month == 0:
        month = 12
        year -= 1
    return redirect('/mccalendar/%s/%s/' % (year, month))

  cur_year, cur_month, cur_day = time.localtime()[:3]

  cal = calendar.Calendar()
  cal.setfirstweekday(calendar.SUNDAY)
  month_days = cal.itermonthdays(year, month)

  events = []
  lst=[[]]
  week = 0

  for day in month_days:
    entries = current = False
    if day:
      events = McEvent.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)
      if day == cur_day and year == cur_year and month == cur_month:
        current = True
    lst[week].append((day, events, current))
    if len(lst[week]) == 7:
      lst.append([])
      week += 1
  context = {
    'year': year,
    'month': month,
    'day': day,
    'month_name': month_names[month-1],
    'month_days': lst,
  }
  return render(request, 'mccalendar/month.html', context)

@login_required
def day(request, year=None, month=None, day=None):
  year = int(year) if year else time.localtime()[0]
  month = int(month) if month else time.localtime()[1]

  events = McEvent.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)
  context = {
    'year': year,
    'month': month,
    'day': day,
    'month_name': month_names[month-1],
    'events': events,
  }
  return render(request, 'mccalendar/day.html', context)

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