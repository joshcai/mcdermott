import csv
import datetime
import random
import string
import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.models import Degree, Experience, McUser

import requests

try:
  from mcdermott.config import DEFAULT_PASSWORD
except ImportError:
  from mcdermott.example_config import DEFAULT_PASSWORD
from mcdermott.roles import Staff, Scholar, CurrentScholar, Dev, Selection

def randomString():
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class Command(BaseCommand):
  help = 'Seeds with some default users'

  def add_arguments(self, parser):

    parser.add_argument('--flush',
        action='store_true',
        dest='flush',
        default=False,
        help='Remove all users first')

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

    parser.add_argument('--alumni',
        action='store_true',
        dest='alumni',
        default=False,
        help='Create alumni accounts')

    parser.add_argument('--alumnifull',
        action='store_true',
        dest='alumnifull',
        default=False,
        help='Create rest of alumni accounts')

    parser.add_argument('--degrees',
        action='store_true',
        dest='degrees',
        default=False,
        help='Seed degrees from UTD')
        
  def add_user(self, username, password, name, class_year, birthday='1/1/2000', superuser=False, email=None):
    if User.objects.filter(username=username).exists():
      user = User.objects.get(username=username)
      self.stdout.write('Account for user %s already exists' % username)
    else:
      if superuser:
        user = User.objects.create_superuser(username, email, password)
      else:
        user = User.objects.create_user(username, email=email, password=password)
      self.stdout.write('Added user %s - username: %s, password: %s' %
                        (name, username, password))
    first, last = name.split()
    user.mcuser.first_name = first
    user.mcuser.last_name = last
    user.mcuser.class_year = class_year
    user.mcuser.save()
    return user

  def convertDate(self, date):
    # Converts from 09/24/15 to 2015-24-09
    return datetime.datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')

  def getUsername(self, email):
    return email.split('@')[0].lower()

  def add_from_csv(self, scholar):
    if not scholar['UTD email']:
      self.stdout.write('No email found for %s' % (scholar['V3']))
      return
    username = self.getUsername(scholar['UTD email'])
    if User.objects.filter(username=username).exists():
      self.stdout.write('Account for user %s already exists' % scholar['V3'])
      user = User.objects.get(username=username)
    else:
      user = User.objects.create_user(username, email=scholar['UTD email'].lower(), password=randomString())
    user.mcuser.real_name = scholar['First']
    user.mcuser.first_name = scholar['Pref First']
    user.mcuser.middle_name = scholar['Middle']
    user.mcuser.last_name = scholar['Last']
    user.mcuser.gender = ('Male' if scholar['Title'] == 'Mr.' else 'Female')
    user.mcuser.class_year = scholar['Class']
    if scholar['DOB']:
      user.mcuser.birthday = self.convertDate(scholar['DOB'])
    user.mcuser.email = scholar['UTD email']
    user.mcuser.phone_number = scholar['Cell']
    user.mcuser.save()
    CurrentScholar.assign_role_to_user(user)
    Scholar.assign_role_to_user(user)
    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))

  def add_staff_from_csv(self, staff):
    username = self.getUsername(staff['Email'])
    if User.objects.filter(username=username).exists():
      self.stdout.write('Account for user %s %s already exists' % (staff['First'], staff['Last']))
      user = User.objects.get(username=username)
    else:
      user = User.objects.create_user(username, email=staff['Email'].lower(), password=randomString())
    user.mcuser.real_name = staff['Real']
    user.mcuser.first_name = staff['First']
    user.mcuser.last_name = staff['Last']
    user.mcuser.gender = staff['Gender']
    user.mcuser.email = staff['Email']
    user.mcuser.staff_title = staff['Title']
    user.mcuser.staff_phone = staff['Phone']
    user.mcuser.staff_order = staff['Order']
    user.mcuser.save()
    Staff.assign_role_to_user(user)
    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))


  def add_alumni_from_csv(self, alumni):
    username = self.getUsername(alumni['Email'])
    if User.objects.filter(username=username).exists():
      self.stdout.write('Account for user %s %s already exists' % (alumni['First'], alumni['Last']))
      user = User.objects.get(username=username)
    else:
      user = User.objects.create_user(username, email=alumni['Email'].lower(), password=DEFAULT_PASSWORD)
    if alumni['Year'] != 'None':
      user.mcuser.class_year = int(alumni['Year'])
    user.mcuser.first_name = alumni['First']
    user.mcuser.last_name = alumni['Last']
    user.mcuser.email = alumni['Email']
    user.mcuser.save()
    if alumni['Selection'] == 'True':
      Selection.assign_role_to_user(user)
    session = requests.session()
    url = 'http://mcdermott.org/password_reset'
    response = session.get(url)
    csrftoken = session.cookies['csrftoken']
    # r = session.post(
    #  url,
    #  data={'email': user.email, 'csrfmiddlewaretoken': csrftoken},
    #  headers=dict(Referer=url))
    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))

  def add_alumni_full_from_csv(self, alumni):
    username = self.getUsername(alumni['Email'])
    combined = '%s %s' % (alumni['Last'], alumni['Married Name'])
    if User.objects.filter(username=username).exists():
      self.stdout.write('Account for user %s %s already exists' % (alumni['First'], alumni['Last']))
      user = User.objects.get(username=username)
    elif McUser.objects.filter(first_name=alumni['First'], last_name=alumni['Last']).exists():
      self.stdout.write('Account for user %s %s already exists' % (alumni['First'], alumni['Last']))
      user = McUser.objects.get(first_name=alumni['First'], last_name=alumni['Last']).user
    elif McUser.objects.filter(first_name=alumni['First'], last_name=combined).exists():
      self.stdout.write('Account for user %s %s already exists' % (alumni['First'], combined))
      user = McUser.objects.get(first_name=alumni['First'], last_name=combined).user
    else:
      user = User.objects.create_user(username, email=alumni['Email'].lower(), password=DEFAULT_PASSWORD)
    if alumni['Class'] != 'None':
      user.mcuser.class_year = int(alumni['Class'])
    user.mcuser.first_name = alumni['First']
    if alumni['Married Name']:
      user.mcuser.last_name = alumni['Married Name']
      user.mcuser.maiden_name = alumni['Last']
    else:
      user.mcuser.last_name = alumni['Last']
    user.mcuser.email = alumni['Email']
    user.mcuser.married = True if alumni['marriage'] else False
    user.mcuser.num_degrees = int(alumni['num grad degrees']) if alumni['num grad degrees'] else 0
    user.mcuser.right_after = alumni['right_after']
    user.mcuser.ultimate = alumni['ultimate']
    user.mcuser.updated_alumni_info = alumni['updated alumni info'].split(' ')[0]
    user.mcuser.updated_alumni_ppt = alumni['updated alumni ppt']
    user.mcuser.mailing_address = alumni['Address']
    user.mcuser.mailing_city = alumni['City']
    user.mcuser.mailing_state = alumni['State']
    user.mcuser.mailing_zip = alumni['Zip']
    user.mcuser.mailing_country = alumni['Country']
    user.mcuser.mailing_address_type = alumni['address type']
    user.mcuser.address_type = alumni['address type']
    user.mcuser.phone_number = alumni['Phone']
    user.mcuser.website = alumni['Website']
    user.mcuser.in_dfw = alumni['Currently in DFW']
    user.mcuser.current_city = alumni['Current City']
    user.mcuser.significant_other = alumni['Significant other']
    user.mcuser.children = alumni['Children']
    user.mcuser.personal_news = alumni['Personal News']
    m = user.mcuser
    if m.degrees.count() == 0:
      if alumni['Graduate School #1']:
        d = Degree(
            user=m,
            school=alumni['Graduate School #1'],
            degree_type=alumni['Degree #1'],
            major1=alumni['Field #1']
          )
        d.save()
      if alumni['Graduate School #2']:
        d = Degree(
            user=m,
            school=alumni['Graduate School #2'],
            degree_type=alumni['Degree #2'],
            major1=alumni['Field #2']
          )
        d.save()
      if alumni['Graduate School #3']:
        d = Degree(
            user=m,
            school=alumni['Graduate School #3'],
            degree_type=alumni['Degree #3'],
            major1=alumni['Field #3']
          )
        d.save()
    if m.experiences.count() == 0:
      if alumni['Previous Employment']:
        exps = alumni['Previous Employment'].split(';')
        for exp in exps:
          loc_split = exp.split('(')
          if len(loc_split) == 2:
            e = Experience(
                user=m,
                organization=loc_split[0],
                location=loc_split[1].strip(' ').strip(')')
              )
          else:
            e = Experience(
                user=m,
                organization=exp
              )
          e.save()
      if alumni['Current Employment']:
        exp = alumni['Current Employment']
        loc_split = exp.split('(')
        if len(loc_split) == 2:
          e = Experience(
              user=m,
              organization=loc_split[0],
              location=loc_split[1].strip(' ').strip(')')
            )
        else:
          e = Experience(
              user=m,
              organization=exp
            )
          e.save()
    user.mcuser.hidden_fields = ['phone_number', 'email', 'address']
    user.mcuser.save()

    self.stdout.write('Created user %s %s' %
                      (user.mcuser.first_name, user.mcuser.last_name))

  def add_degree(self, alumni):
    full_name = alumni['NAME']
    last, first = full_name.split(',')
    last = last.strip()
    first = first.strip().split(' ')[0].strip()
    
    if McUser.objects.filter(first_name=first, last_name=last).exists():
      self.stdout.write('Account for user %s %s found' % (first, last))
      m = McUser.objects.get(first_name=first, last_name=last)
    elif McUser.objects.filter(first_name__startswith=first, maiden_name=last).exists():
      self.stdout.write('Account for user %s %s found' % (first, last))
      m = McUser.objects.get(first_name__startswith=first, maiden_name=last)
    else:
      self.stdout.write('!!! Account for user %s %s not found !!!' % (first, last))
      return
    d = Degree(
        user=m,
        school='University of Texas at Dallas',
        degree_type=alumni['DEGREE'],
        major1=alumni['MAJOR1'].strip(),
        major2=alumni['MAJOR2'].strip(),
        minor1=alumni['MINOR1'].strip(),
        minor2=alumni['MINOR2'].strip(),
      )
    d.save()

    self.stdout.write('Added degree')


  def handle(self, *args, **options):
    if options['flush']:
      self.stdout.write('Deleting all users...')
      User.objects.all().delete()
      self.stdout.write('%s users in the database' % User.objects.all().count())
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
    if options['alumni']:
      with open('alumni_fw.csv', 'rB') as csvfile:
        alumni_members = list(csv.reader(csvfile))
        for alumni in alumni_members[1:]:
          self.add_alumni_from_csv({key: value for (key, value) in zip(alumni_members[0], alumni)})
    if options['alumnifull']:
      with open('alumni_full.csv', 'rB') as csvfile:
        alumni_members = list(csv.reader(csvfile))
        for alumni in alumni_members[1:]:
          self.add_alumni_full_from_csv({key: value for (key, value) in zip(alumni_members[0], alumni)})
    if options['degrees']:
      with open('degrees.csv', 'rB') as csvfile:
        alumni_members = list(csv.reader(csvfile))
        for alumni in alumni_members[1:]:
          self.add_degree({key: value for (key, value) in zip(alumni_members[0], alumni)})
    if options['testing']:
      josh = self.add_user('joshcai', 'password', 'Josh Cai', 2012, email='jxc124730@utdallas.edu')
      Dev.assign_role_to_user(josh)
      staff = self.add_user('staff', 'password', 'Staff User', 2012)
      Staff.assign_role_to_user(staff)
      self.add_user('atvaccaro', 'password', 'Andrew Vaccaro', 2013, email='andrew.vaccaro@utdallas.edu')
      self.add_user('hajieren', 'password', 'Hans Ajieren', 2014)
      self.add_user('dhruvn', 'password', 'Dhruv Narayanan', 2014)
      self.add_user('admin', 'password', 'Admin User', 2000, superuser=True,
                    email='admin@test.com')
