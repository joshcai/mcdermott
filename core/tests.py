from django.contrib.auth.models import User
from django.test import TestCase, Client


class CoreTestCase(TestCase):

  def setUp(self):
    self.app = Client()
    self.user = User.objects.create_user('test', 'a@a.com', 'password')
    self.user.first_name = 'Test'
    self.user.last_name = 'Name'
    self.user.save()

  def testGetFullName(self):
    self.assertEqual(self.user.get_full_name(), 'Test Name')

  def testMcUserGetsCreated(self):
    self.assertIsNotNone(self.user.mcuser)

