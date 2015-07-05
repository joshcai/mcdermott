from django.contrib.auth.models import User
from django.test import TestCase, Client


class LoginTestCase(TestCase):

  def setUp(self):
    self.app = Client()
    self.user = User.objects.create_user('test', 'a@a.com', 'password')

  def testLoginRenders(self):
    response = self.app.get('/login/')
    self.assertEqual(response.status_code, 200)

  def testLogoutRenders(self):
    self.app.login(username='test', password='password')
    response = self.app.get('/logout/')
    self.assertEqual(response.status_code, 302)