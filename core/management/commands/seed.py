from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
  help = 'Seeds with some default users'

  def add_user(self, username, password, name, superuser=False, email=None):
    if User.objects.filter(username=username).exists():
      self.stdout.write('User %s already exists' % username)
      return
    if superuser:
      user = User.objects.create_superuser(username, email, password)
    else:
      user = User.objects.create_user(username, password=password)
    first, last = name.split()
    user.first_name = first
    user.last_name = last
    user.save()
    self.stdout.write('Added user %s - username: %s, password: %s' % 
                      (name, username, password))

  def handle(self, *args, **options):
    self.add_user('joshcai', 'password', 'Josh Cai')
    self.add_user('atvaccaro', 'password', 'Andrew Vaccaro')
    self.add_user('hajieren', 'password', 'Hans Ajieren')
    self.add_user('admin', 'password', 'Admin User', superuser=True, 
                  email='admin@test.com')
