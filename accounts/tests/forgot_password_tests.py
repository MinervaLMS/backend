from django.test import TestCase
from rest_framework.test import APIClient

from courses.models import Course
from institutions.models import Institution


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(
            name="Universidad Nacional de Colombia",
            alias="UNAL",
            description="UNAL description",
            url="https://unal.edu.co/",
        )
        self.course = Course.objects.create(
            name="Estructuras de Datos",
            alias="ED",
            institution=self.institution,
        )
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.incorrect_credentials = {"email": "test1@example.com"}

    def test_password_reset_correct(self):
        self.client.post("/register/", self.user_data, format="json")
        response = self.client.post(
            "/forgot-my-password/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_incorrect(self):
        self.client.post("/register/", self.user_data, format="json")
        response = self.client.post(
            "/forgot-my-password/", self.incorrect_credentials, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_password_reset_blank(self):
        self.client.post("/register/", self.user_data, format="json")
        response = self.client.post("/forgot-my-password/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_password_reset_no_user(self):
        response = self.client.post(
            "/forgot-my-password/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 404)
