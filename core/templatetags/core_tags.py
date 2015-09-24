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
  if len(value) < 10:
    return value
  return '(%s) %s-%s' % (value[:3], value[3:6], value[6:])
