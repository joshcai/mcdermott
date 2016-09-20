from django.contrib.auth.models import User
from django.test import TestCase, Client


class CoreTestCase(TestCase):

  def setUp(self):
    self.app = Client()
    self.user = User.objects.create_user('test', 'a@a.com', 'password')
    self.user.save()
    self.user.mcuser.first_name = 'Test'
    self.user.mcuser.last_name = 'Name'
    self.user.mcuser.save()

  def login(self):
    self.app.login(username='test', password='password')    

  def testGetFullName(self):
    self.assertEqual(self.user.mcuser.get_full_name(), 'Test Name')

  def testMcUserGetsCreated(self):
    self.assertIsNotNone(self.user.mcuser)

  def testSearchRedirectIfOneResult(self):
    self.login()
    response = self.app.get('/search?q=Test')
    self.assertRedirects(response, '/testname')

  def testSearchMoreThanOneResult(self):
    self.login()
    # Create second user with first name 'Test'
    u = User.objects.create_user('test2', 'b@b.com', 'password')
    u.save()
    u.mcuser.first_name = 'Test'
    u.mcuser.last_name = 'Foo'
    u.mcuser.save()

    response = self.app.get('/search?q=Test')
    self.assertIn('Test Name', response.content)
    self.assertIn('Test Foo', response.content)

  def testReindexing(self):
    self.login()
    response = self.app.get('/search?q=Test')
    self.assertRedirects(response, '/testname')
    self.user.mcuser.first_name = 'Foo'
    self.user.mcuser.save()
    response = self.app.get('/search?q=Foo')
    self.assertRedirects(response, '/fooname')
