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
  return value.replace(' ', '').replace('\'', '')

@register.filter
def fieldhidden(value, field):
  # value is a McUser object
  return field in value.hidden_fields

@register.filter
def absoluteurl(url):
  if url.startswith('http://') or url.startswith('https://'):
    return url
  return 'http://%s' % url

@register.filter
def pwrap(value):
  lines = value.split('\n')
  return ''.join(['<p>%s</p>' % line for line in lines])

@register.inclusion_tag('macro/directory_header.html')
def directory_header(active):
  return {'active': active, 'class_years': [str(x) for x in range(2001, 2016)]}
