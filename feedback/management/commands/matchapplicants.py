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
