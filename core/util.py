# Utility functions used by multiple modules

def normalize_name(name):
  return ''.join([c.lower() for c in name if c.isalpha()])