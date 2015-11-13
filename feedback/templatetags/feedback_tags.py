from django import template

import random

from feedback.models import Feedback

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
  return '%d' % len(non_empty)

@register.filter
def all_feedback(applicant):
  return Feedback.objects.filter(applicant=applicant)

@register.inclusion_tag('macro/feedback_header.html')
def feedback_header(active, user):
  return {'active': active, 'user': user}
