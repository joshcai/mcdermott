import csv
import os
import random
import shutil
import string
from urlparse import urlparse, parse_qs

import requests

from localflavor.us.us_states import US_STATES

from django.core.files import File
from django.core.management.base import BaseCommand
from feedback.models import Applicant, Feedback, Event
from core.models import McUser
from core.util import normalize_name

def randomWords(num_words):
  return ' '.join(randomString(random.randint(4, 10)) for _ in range(num_words)).capitalize()

def randomString(length):
  return ''.join(random.choice(string.ascii_uppercase) for _ in range(length)).capitalize()

class Command(BaseCommand):
  help = 'Seeds with some default applicants'

  def add_arguments(self, parser):

    parser.add_argument('event_name', nargs=1, type=str)

    parser.add_argument('--flush',
        action='store_true',
        dest='flush',
        default=False,
        help='Remove all applicants first')

    parser.add_argument('--applicants',
        action='store_true',
        dest='applicants',
        default=False,
        help='Use CSV from applicants.csv')

    parser.add_argument('--testing',
        action='store_true',
        dest='testing',
        default=False,
        help='Use some test accounts')

    parser.add_argument('--feedback',
        action='store_true',
        dest='feedback',
        default=False,
        help='Seed some random feedback')

    parser.add_argument('--pics',
        action='store_true',
        dest='pics',
        default=False,
        help='Seed some random feedback')

  def add_applicant(self, applicant):
    if Applicant.objects.filter(first_name=applicant['First'], last_name=applicant['Last']).exists():
      self.stdout.write('Account for user %s %s already exists' % (applicant['First'], applicant['Last']))
      app = Applicant.objects.get(first_name=applicant['First'], last_name=applicant['Last'])
    else:
      app = Applicant()
    app.first_name = applicant['First']
    app.last_name = applicant['Last']
    app.high_school = applicant['High School']
    app.hometown = applicant['City']
    app.hometown_state = applicant['State']
    app.gender = applicant['Title']
    if applicant['Picture']:
      url = applicant['Picture']
      old_file_name = parse_qs(urlparse(url).query)['Filename']
      extension = old_file_name[0].split('.')[-1]
      file_name = '%s,%s.%s' % (applicant['Last'], applicant['First'], extension)
      response = requests.get(url, stream=True)
      with open('tmp/%s' % file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
      with open('tmp/%s' % file_name, 'rb') as img_file:
        app.pic.save(file_name, File(img_file), save=True)
    app.save()
    self.stdout.write('Created user %s %s' % (app.first_name, app.last_name))
    return app

  def handle(self, *args, **options):
    print options['event_name'][0]
    if options['flush']:
      self.stdout.write('Deleting all applicants...')
      Applicant.objects.all().delete()
      self.stdout.write('%s users in the database' % Applicant.objects.all().count())
    if options['applicants']:
      if not os.path.exists('tmp'):
        os.makedirs('tmp')
      with open('applicants2.csv', 'rU') as csvfile:
        applicants = list(csv.reader(csvfile))
        event = Event.objects.get(name=options['event_name'][0])
        for applicant in applicants[1:]:
          app = self.add_applicant({key: value for (key, value) in zip(applicants[0], applicant)})
          app.event = event
          app.save()
    if options['testing']:
      for _ in xrange(10):
        applicant = Applicant()
        applicant.first_name = randomString(10)
        applicant.last_name = randomString(10)
        applicant.high_school = '%s High School ' % randomString(8)
        applicant.hometown = randomString(7)
        applicant.hometown_state = random.choice(US_STATES)[0]
        applicant.gender = random.choice(['Mr.', 'Ms.'])
        applicant.save()
        self.stdout.write('Created user %s' % applicant.get_full_name())
    if options['feedback']:
      scholars = McUser.objects.all()
      applicants = Applicant.objects.all()
      for scholar in scholars:
        chance = random.random() / 3
        for applicant in applicants:
          if random.random() < chance:
            try:
              f = Feedback.objects.get(scholar=scholar, applicant=applicant)
            except Feedback.DoesNotExist:
              f = Feedback(scholar=scholar, applicant=applicant)
            f.rating = random.choice([0, 1, 2, 3, 4, 5])
            f.interest = random.choice([0, 1, 3, 4, 5])
            f.comments = randomWords(random.randint(4, 15))
            f.save()
    if options['pics']:
      for f in os.listdir('tmp'):
        f_split = f.split('.')[0].split(',')
        scholar_name = normalize_name('%s%s' % (f_split[1], f_split[0]))
        try:
          app = Applicant.objects.get(norm_name=scholar_name)
        except Applicant.DoesNotExist:
          self.stdout.write('Could not find user %s for pic %s' % (scholar_name, f))
          continue
        extension = f.split('.')[-1]
        file_name = '%s,%s-sp.%s' % (app.last_name, app.first_name, extension)
        with open('tmp/%s' % f, 'rb') as img_file:
          app.actual_pic.save(file_name, File(img_file), save=True)
        app.save()
        self.stdout.write('Saved pic %s for %s' % (f, scholar_name))

