import os

from django.core.files import File
from django.core.management.base import BaseCommand
from feedback.models import Applicant, Feedback, Event, Assignment
from core.models import McUser
from core.util import normalize_name

class Command(BaseCommand):
  help = 'Seeds with some default applicants'

  def add_arguments(self, parser):

    parser.add_argument('event_name', nargs=1, type=str)

    parser.add_argument('--assignments',
        nargs='?',
        dest='assignments',
        default='',
        help='Which file to use for assignments')

    parser.add_argument('--flush',
        action='store_true',
        dest='flush',
        default=False,
        help='Remove all assignments in the event')

  def add_applicant(self, applicant, event_name):
    if Applicant.objects.filter(first_name=applicant['First'], last_name=applicant['Last'], event__name=event_name).exists():
      self.stdout.write('Account for user %s %s already exists' % (applicant['First'], applicant['Last']))
      app = Applicant.objects.get(first_name=applicant['First'], last_name=applicant['Last'], event__name=event_name)
    else:
      app = Applicant()
    app.first_name = applicant.get('First', '')
    app.last_name = applicant.get('Last', '')
    app.high_school = applicant.get('High School', '')
    app.hometown = applicant.get('City', '')
    app.hometown_state = applicant.get('State', '')
    app.gender = applicant.get('Title', '')
    event = Event.objects.get(name=event_name)
    app.event = event
    if applicant.get('Picture', ''):
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
    event_name = options['event_name'][0]
    if options['flush']:
      self.stdout.write('Removing all assignments in event %s...' % event_name)
      self.stdout.write('%s assignments in the database' % Assignment.objects.all().count())
      assignments = Assignment.objects.filter(applicant__event__name=event_name)
      self.stdout.write('%s assignments in the event %s' % (assignments.count(), event_name))
      assignments.delete()
      self.stdout.write('%s assignments left in the database' % Assignment.objects.all().count())
    if options['assignments']:
      self.stdout.write('%s assignments in the database' % Assignment.objects.all().count())
      with open(options['assignments'], 'r') as f:
        applicant = ''
        for i, line in enumerate(f):
          if i % 4 == 0:
            continue
          if i % 4 == 1:
            applicant = line
          if i % 4 == 2:
            applicant = normalize_name('%s%s' % (applicant, line))
          if i % 4 == 3:
            try:
              app = Applicant.objects.get(norm_name=applicant, event__name=event_name)
              scholar = McUser.objects.get(norm_name=normalize_name(line))
              assignment = Assignment(scholar=scholar, applicant=app)
              assignment.save()
            except Applicant.DoesNotExist:
              print 'could not find applicant %s' % applicant
      self.stdout.write('%s assignments in the database' % Assignment.objects.all().count())
