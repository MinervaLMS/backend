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
        response = self.client.post(
            '/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.last().email, 'test@example.com')

    def test_register_blank(self):
        response = self.client.post('/register/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_types(self):
        response = self.client.post(
            '/register/', self.user_data_types, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_repeat(self):
        response1 = self.client.post(
            '/register/', self.user_data, format='json')
        response2 = self.client.post(
            '/register/', self.user_data, format='json')
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
        register = self.client.post(
            '/register/', self.user_data, format='json')
        response = self.client.post(
            '/forgot-my-password/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_incorrect(self):
        register = self.client.post(
            '/register/', self.user_data, format='json')
        response = self.client.post(
            '/forgot-my-password/', self.incorrect_credentials, format='json')
        self.assertEqual(response.status_code, 404)

    def test_password_reset_blank(self):
        register = self.client.post(
            '/register/', self.user_data, format='json')
        response = self.client.post('/forgot-my-password/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_password_reset_no_user(self):
        response = self.client.post(
            '/forgot-my-password/', self.user_data, format='json')
        self.assertEqual(response.status_code, 404)


class GetUsersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com', password='testpassword')

    def test_users_list_correct(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_users_list_no_auth(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)


class ContactSupportTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'sender_email': 'test@example.com',
            'sender_name': 'John Doe',
            'subject': 'Test subject',
            'email_body': 'Test email body'
        }
        self.user_bad_email = {
            'sender_email': 'test.example.com',
            'sender_name': 'John Doe',
            'subject': 'Test subject',
            'email_body': 'Test email body'
        }

    def test_contact_support_correct(self):
        response = self.client.post('/contact/', self.user_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_contact_support_bad_email(self):
        response = self.client.post(
            '/contact/', self.user_bad_email, format='json')
        self.assertEqual(response.status_code, 400)

    def test_contact_support_blank(self):
        response = self.client.post('/contact/', {}, format='json')
        self.assertEqual(response.status_code, 400)
