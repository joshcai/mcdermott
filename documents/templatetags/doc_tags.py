
from django import template

register = template.Library()

@register.filter
def normalize_category(name):
  return name.split()[0].lower()
