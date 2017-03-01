import os
import random
import copy

from django.core.files import File
from django.core.management.base import BaseCommand
from feedback.models import Applicant, Feedback, Event, Assignment
from core.models import McUser
from core.util import normalize_name

class Command(BaseCommand):
  help = 'Seeds with some default applicants'

  def add_arguments(self, parser):

    parser.add_argument('event_name', nargs=1, type=str)

    parser.add_argument('--users',
        nargs='?',
        dest='assignments',
        default='',
        help='Which file to use for assignments')

    parser.add_argument('--flush',
        action='store_true',
        dest='flush',
        default=False,
        help='Remove all assignments in the event')

  def flush(self, event_name):
    self.stdout.write('Removing all assignments in event %s...' % event_name)
    self.stdout.write('%s assignments in the database' % Assignment.objects.all().count())
    assignments = Assignment.objects.filter(applicant__event__name=event_name)
    self.stdout.write('%s assignments in the event %s' % (assignments.count(), event_name))
    assignments.delete()
    self.stdout.write('%s assignments left in the database' % Assignment.objects.all().count())

  def assign(self, event_name, users_file):
    self.stdout.write('%s assignments in the database' % Assignment.objects.all().count())
    applicants = Applicant.objects.filter(event__name=event_name)[::1]
    self.stdout.write('%s applicants in the database' % len(applicants))
    with open(users_file, 'r') as f:
      users = [normalize_name(u) for _, u in enumerate(f)]
    self.stdout.write('%s' % users)
    current_list = copy.deepcopy(applicants)
    for u in users:
      user = McUser.objects.get(norm_name=u)
      self.stdout.write(user.get_full_name())
      for _ in xrange(8):
        if len(current_list) == 0:
          current_list = copy.deepcopy(applicants)
        index = random.randint(0, len(current_list)-1)
        applicant = current_list[index]
        assignment = Assignment(scholar=user, applicant=applicant) 
        assignment.save()
        self.stdout.write(' - %s' % applicant.get_full_name())
        del current_list[index]
    self.stdout.write('%s assignments in the database' % Assignment.objects.all().count()) 

  def handle(self, *args, **options):
    event_name = options['event_name'][0]
    if options['flush']:
      self.flush(event_name)
    if options['assignments']:
      random.seed() 
      self.assign(event_name, options['assignments'])

