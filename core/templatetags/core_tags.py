import re

from django import template

register = template.Library()

#http://stackoverflow.com/questions/16450124/how-to-display-2-thumbnails-of-span6-per-row-in-bootstrap-with-django?rq=1
@register.filter
def group_by(value, arg):
  return grouped(value, arg)

def grouped(l, n):
  # Yield successive n-sized chunks from l.
  for i in xrange(0, len(l), n):
      yield l[i:i+n]

@register.filter
def displayphone(value):
  norm_value = re.sub(r'\D', '', value)
  if len(norm_value) != 10:
    return value
  return '(%s) %s-%s' % (norm_value[:3], norm_value[3:6], norm_value[6:])

@register.filter
def removespaces(value):
  return value.replace(' ', '')