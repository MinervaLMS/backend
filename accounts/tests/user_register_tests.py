from django.test import TestCase
from rest_framework.test import APIClient

from ..models.user import User
from courses.models import Course
from institutions.models import Institution


class RegisterTestCase(TestCase):
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
        self.user_data_types = {
            "email": "test@example.com",
            "password": False,
            "first_name": 1,
            "last_name": 3.1416,
        }

    def test_register_correct(self):
        response = self.client.post("/register/", self.user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.last().email, "test@example.com")

    def test_register_blank(self):
        response = self.client.post("/register/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_register_types(self):
        response = self.client.post("/register/", self.user_data_types, format="json")
        self.assertEqual(response.status_code, 400)

    def test_register_repeat(self):
        response1 = self.client.post("/register/", self.user_data, format="json")
        response2 = self.client.post("/register/", self.user_data, format="json")
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)
