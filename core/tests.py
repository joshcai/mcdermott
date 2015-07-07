from django.contrib.auth.models import User
from django.test import TestCase, Client


class CoreTestCase(TestCase):

  def setUp(self):
    self.app = Client()
    self.user = User.objects.create_user('test', 'a@a.com', 'password')
    self.user.first_name = 'Test'
    self.user.last_name = 'Name'
    self.user.save()

  def login(self):
    self.app.login(username='test', password='password')    

  def testGetFullName(self):
    self.assertEqual(self.user.get_full_name(), 'Test Name')

  def testMcUserGetsCreated(self):
    self.assertIsNotNone(self.user.mcuser)

  def testSearchWorks(self):
    self.login()
    response = self.app.get('/search?q=Test')
    self.assertIn('Test Name', response.content)

  def testReindexingWorks(self):
    self.login()
    response = self.app.get('/search?q=Test')
    self.assertIn('Test Name', response.content)
    self.user.first_name = 'Foo'
    self.user.save()
    response = self.app.get('/search?q=Foo')
    self.assertIn('Foo Name', response.content)
