from django.test import TestCase
from rest_framework.test import APIClient

from ..models.user import User
from courses.models import Course


class GetUsersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
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
