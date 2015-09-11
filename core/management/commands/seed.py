from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
  help = 'Seeds with some default users'

  def add_user(self, username, password, name, class_year, birthday="1/1/2000", superuser=False, email=None):
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

  def handle(self, *args, **options):
    self.add_user('joshcai', 'password', 'Josh Cai', 2012)
    self.add_user('dhruvn', 'password', 'Dhruv Narayanan', 2014)
    self.add_user('atvaccaro', 'password', 'Andrew Vaccaro', 2013)
    self.add_user('hajieren', 'password', 'Hans Ajieren', 2014)
    self.add_user('admin', 'password', 'Admin User', 2000, superuser=True,
                  email='admin@test.com')
