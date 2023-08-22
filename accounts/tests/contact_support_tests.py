from django.test import TestCase
from rest_framework.test import APIClient

from ..models import User
from courses.models import Course

class ContactSupportTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
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
