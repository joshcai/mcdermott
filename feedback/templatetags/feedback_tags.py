from django import template

import random

from feedback.models import Feedback, Favorite, Event

register = template.Library()

@register.filter
def rating_average(feedback, num=False):
  ratings = [f.rating for f in feedback if f.rating]
  if not ratings:
    return ''
  avg = sum(ratings) / float(len(ratings))
  if num:
    return avg
  return '%.2f' % avg

@register.filter
def interest_average(feedback, num=False):
  ratings = [f.interest for f in feedback if f.interest]
  if not ratings:
    return ''
  avg = sum(ratings) / float(len(ratings))
  if num:
    return avg
  return '%.2f' % avg

@register.filter
def feedback_count(feedback):
  non_empty = [f for f in feedback if (f.interest or f.rating or f.comments)]
  return str(len(non_empty))

@register.filter
def all_feedback(applicant):
  feedback = Feedback.objects.filter(applicant=applicant)
  return [f for f in feedback]

@register.filter
def alumni_filter(feedback):
  return [f for f in feedback if (f.scholar.class_year < 2013 or f.scholar.class_year is None)]

@register.filter
def senior_filter(feedback):
  return [f for f in feedback if f.scholar.class_year == 2013]

@register.filter
def other_filter(feedback):
  return [f for f in feedback if f.scholar.class_year > 2013]

@register.filter
def favorite_filter(applicant):
  favs = Favorite.objects.filter(applicant=applicant)
  return [f for f in favs]

@register.inclusion_tag('macro/feedback_header.html')
def feedback_header(active, user, event_name):
  return {'active': active, 'user': user, 'event_name': event_name}

@register.inclusion_tag('macro/form_element.html')
def form_element(element, label, style, add_form_control=True):
  return {'element': element, 'style': style, 'label': label, 'add_form_control': add_form_control}

@register.filter
def convert_attended(attended):
  return 'Yes' if attended else 'No'

# works on the Django user, not McUser
@register.filter
def is_staff_for(user, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    return False
  return user.mcuser in event.staff.all()

@register.filter
def can_read_data_for(user, event_name):
  try:
    event = Event.objects.get(name=event_name)
  except Event.DoesNotExist:
    return False
  return user.mcuser in event.staff.all() or user.mcuser in event.selection.all()