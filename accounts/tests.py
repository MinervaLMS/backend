from django.test import TestCase
from rest_framework.test import APIClient

from .models import User

class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.user_data_types = {
            'email': 'test@example.com',
            'password': False,
            'first_name': 1,
            'last_name': 3.1416
        }

    def test_register_correct(self):
        response = self.client.post('/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.last().email, 'test@example.com')

    def test_register_blank(self):
        response = self.client.post('/register/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_types(self):
        response = self.client.post('/register/', self.user_data_types, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_repeat(self):
        response1 = self.client.post('/register/', self.user_data, format='json')
        response2 = self.client.post('/register/', self.user_data, format='json')
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.incorrect_credentials = {
            'email': 'test@example.com',
            'password': 'testpassword1',
        }

    def test_login_correct(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_incorrect(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/login/', self.incorrect_credentials, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_blank(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/login/', {}, format='json')
        self.assertEqual(response.status_code, 400)

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.incorrect_credentials = {
            'email': 'test1@example.com'
        }

    def test_password_reset_correct(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/forget-password/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_incorrect(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/forget-password/', self.incorrect_credentials, format='json')
        self.assertEqual(response.status_code, 404)

    def test_password_reset_blank(self):
        register = self.client.post('/register/', self.user_data, format='json')
        response = self.client.post('/forget-password/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_password_reset_no_user(self):
        response = self.client.post('/forget-password/', self.user_data, format='json')
        self.assertEqual(response.status_code, 404)
