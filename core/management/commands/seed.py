import csv
import datetime
import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from mcdermott.roles import Staff, Scholar, CurrentScholar

class Command(BaseCommand):
  help = 'Seeds with some default users'

  def add_arguments(self, parser):

    parser.add_argument('--scholars',
        action='store_true',
        dest='scholars',
        default=False,
        help='Use CSV from scholars.csv')

    parser.add_argument('--staff',
        action='store_true',
        dest='staff',
        default=False,
        help='Use CSV from staff.csv')

    parser.add_argument('--testing',
        action='store_true',
        dest='testing',
        default=False,
        help='Use some test accounts')

  def add_user(self, username, password, name, class_year, birthday='1/1/2000', superuser=False, email=None):
    if User.objects.filter(username=username).exists():
      self.stdout.write('User %s already exists' % username)
      return
    if superuser:
      user = User.objects.create_superuser(username, email, password)
    else:
      user = User.objects.create_user(username, password=password)
    first, last = name.split()
    user.mcuser.first_name = first
    user.mcuser.last_name = last
    user.mcuser.class_year = class_year
    user.mcuser.save()
    self.stdout.write('Added user %s - username: %s, password: %s' %
                      (name, username, password))

  def convertDate(self, date):
    # Converts from 09/24/15 to 2015-24-09
    return datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')

  def add_from_csv(self, scholar):
    if not scholar['UTD email']:
      self.stdout.write('No email found for %s' % (scholar['V3']))
      return
    if User.objects.filter(username=scholar['UTD email'].lower()).exists():
      self.stdout.write('Account for user %s already exists' % scholar['V3'])
      user = User.objects.get(username=scholar['UTD email'].lower())
    else:
      user = User.objects.create_user(scholar['UTD email'].lower(), email=scholar['UTD email'].lower(), password='password')
    user.mcuser.real_name = scholar['First']
    user.mcuser.first_name = scholar['Pref First']
    user.mcuser.middle_name = scholar['Middle']
    user.mcuser.last_name = scholar['Last']
    user.mcuser.gender = ('Male' if scholar['Title'] == 'Mr.' else 'Female')
    user.mcuser.class_year = scholar['Class']
    user.mcuser.birthday = self.convertDate(scholar['DOB'])
    user.mcuser.phone_number = scholar['Cell']
    user.mcuser.save()
    CurrentScholar.assign_role_to_user(user)
    Scholar.assign_role_to_user(user)
    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))

  def add_staff_from_csv(self, staff):
    if User.objects.filter(username=staff['Email'].lower()).exists():
      self.stdout.write('Account for user %s %s already exists' % (staff['First'], staff['Last']))
      user = User.objects.get(username=staff['Email'].lower())
    else:
      user = User.objects.create_user(staff['Email'].lower(), email=staff['Email'].lower(), password='password')
    user.mcuser.real_name = staff['Real']
    user.mcuser.first_name = staff['First']
    user.mcuser.last_name = staff['Last']
    user.mcuser.gender = staff['Gender']
    user.mcuser.staff_title = staff['Title']
    user.mcuser.staff_phone = staff['Phone']
    user.mcuser.save()
    Staff.assign_role_to_user(user)
    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))


  def handle(self, *args, **options):
    if options['scholars']:
      with open('scholars.csv', 'rU') as csvfile:
        scholars = list(csv.reader(csvfile))
        for scholar in scholars[1:]:
          self.add_from_csv({key: value for (key, value) in zip(scholars[0], scholar)})
    if options['staff']:
      with open('staff.csv', 'rB') as csvfile:
        staff_members = list(csv.reader(csvfile))
        for staff in staff_members[1:]:
          self.add_staff_from_csv({key: value for (key, value) in zip(staff_members[0], staff)})
    if options['testing']:
      self.add_user('joshcai', 'password', 'Josh Cai', 2012, email='jxc124730@utdallas.edu')
      self.add_user('atvaccaro', 'password', 'Andrew Vaccaro', 2013, email='andrew.vaccaro@utdallas.edu')
      self.add_user('hajieren', 'password', 'Hans Ajieren', 2014)
      self.add_user('dhruvn', 'password', 'Dhruv Narayanan', 2014)
      self.add_user('admin', 'password', 'Admin User', 2000, superuser=True,
                    email='admin@test.com')
