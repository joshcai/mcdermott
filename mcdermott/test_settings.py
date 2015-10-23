# Settings for running unit tests
# python manage.py test --settings=mcdermott.settings

from settings import *

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}