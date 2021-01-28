from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class LoginTestCase(TestCase):

    def test_login(self):
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/login.html')

    def test_logout(self):
        client = Client()
        response = client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup/logout.html')

    def test_signup(self):
        client = Client()
        response = client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')