from django.test import TestCase
from rest_framework.test import APIClient

from ..models.user import User
from courses.models.course import Course
from institutions.models.institution import Institution


class GetUsersTestCase(TestCase):
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
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_users_list_correct(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_users_list_no_auth(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 401)


class GetUserTestCase(TestCase):
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
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_user_get_correct(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/users/{self.user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_user_get_no_auth(self):
        response = self.client.get(f"/users/{self.user.id}/")
        self.assertEqual(response.status_code, 401)

    def test_user_get_not_found(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/users/{self.user.id + 1}/")
        self.assertEqual(response.status_code, 404)


class GetUserCoursesTestCase(TestCase):
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
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_user_courses_get_correct(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/users/{self.user.id}/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.course.id,
                    "name": self.course.name,
                    "alias": self.course.alias,
                }
            ],
        )

    def test_user_courses_get_no_auth(self):
        response = self.client.get(f"/users/{self.user.id}/courses/")
        self.assertEqual(response.status_code, 401)

    def test_user_courses_get_not_found(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/users/{self.user.id + 34}/courses/")
        self.assertEqual(response.status_code, 404)
