from django import template

register = template.Library()

@register.filter
def rating_average(feedback):
  ratings = [f.rating for f in feedback if f.rating]
  if not ratings:
    return 'N/A'
  return '%.2f' % (sum(ratings) / float(len(ratings)))

@register.filter
def interest_average(feedback):
  ratings = [f.interest for f in feedback if f.interest]
  if not ratings:
    return 'N/A'
  return '%.2f' % (sum(ratings) / float(len(ratings)))

@register.filter
def feedback_count(feedback):
  non_empty = [f for f in feedback if (f.interest or f.rating or f.comments)]
  if not non_empty:
    return 'N/A'
  return '%d' % len(non_empty)
