from django.test import TestCase
from rest_framework.test import APIClient

from ..models import User
from courses.models import Course

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
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
        register = self.client.post(
            '/register/', self.user_data, format='json')

        user_confirm_data = register.json()
        token = user_confirm_data['token']
        uidb64 = user_confirm_data['uidb64']
        confirm_email = self.client.post(
            f'/register/confirm/{uidb64}/{token}', {}, format='json')

        response = self.client.post('/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_incorrect(self):
        register = self.client.post(
            '/register/', self.user_data, format='json')
        response = self.client.post(
            '/login/', self.incorrect_credentials, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_blank(self):
        register = self.client.post(
            '/register/', self.user_data, format='json')
        response = self.client.post('/login/', {}, format='json')
        self.assertEqual(response.status_code, 400)
