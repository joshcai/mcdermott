import random
import string

from localflavor.us.us_states import US_STATES

from django.core.management.base import BaseCommand
from feedback.models import Applicant


def randomString(length):
  return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

class Command(BaseCommand):
  help = 'Seeds with some default applicants'

  def add_arguments(self, parser):

    parser.add_argument('--flush',
        action='store_true',
        dest='flush',
        default=False,
        help='Remove all applicants first')

  def handle(self, *args, **options):
    if options['flush']:
      self.stdout.write('Deleting all applicants...')
      Applicant.objects.all().delete()
      self.stdout.write('%s users in the database' % Applicant.objects.all().count())
    for _ in xrange(10):
      applicant = Applicant()
      applicant.first_name = randomString(10)
      applicant.last_name = randomString(10)
      applicant.high_school = '%s High School ' % randomString(14)
      applicant.hometown = randomString(7)
      applicant.hometown_state = random.choice(US_STATES)[0]
      applicant.gender = random.choice(['Male', 'Female'])
      applicant.save()
      self.stdout.write('Created user %s' % applicant.get_full_name())
