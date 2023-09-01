from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material
from ..models.material_html import MaterialHTML

from accounts.models.user import User


class CreateMaterialHTMLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="HTM",
            is_extra=True,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.material_html_data = {
            "material_id": self.material.id,
            "content": "Test markdown content",
        }

        self.material_html_no_material_data = {
            "material_id": self.material.id + 1,
            "content": "Test markdown content",
        }

        self.material_html_data_invalid = {
            "material_id": True,
            "content": 1,
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self):
        response = self.client.post(
            "/material/html/create/", self.material_html_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_blank(self):
        response = self.client.post("/material/html/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_no_material(self):
        response = self.client.post(
            "/material/html/create/", self.material_html_no_material_data, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_repeat(self):
        self.client.post(
            "/material/html/create/", self.material_html_data, format="json"
        )
        response2 = self.client.post(
            "/material/html/create/", self.material_html_data, format="json"
        )
        self.assertEqual(response2.status_code, 400)

    def test_create_invalid_types(self):
        response = self.client.post(
            "/material/html/create/", self.material_html_data_invalid, format="json"
        )
        self.assertEqual(response.status_code, 400)


class GetMaterialHTMLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="HTM",
            is_extra=True,
        )
        self.material_html = MaterialHTML.objects.create(
            material_id=self.material,
            content="Test markdown content",
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.client.force_authenticate(self.user)

    def test_get_material_html_correct(self):
        response = self.client.get(f"/material/html/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_material_html_not_exist(self):
        response = self.client.get("/material/1122/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateMaterialHTMLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="HTM",
            is_extra=True,
        )
        self.material_html = MaterialHTML.objects.create(
            material_id=self.material,
            content="Test markdown content",
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.material_html_update_data = {
            "content": "Test markdown content update",
        }

        self.material_html_update_data_invalid = {
            "material_id": 999,
        }

        self.client.force_authenticate(self.user)

    def test_update_material_html_correct(self):
        response = self.client.patch(
            f"/material/html/update/{self.material.id}/",
            self.material_html_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_material_html_blank(self):
        response = self.client.patch(
            f"/material/html/update/{self.material.id}/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_material_html_invalid(self):
        response = self.client.patch(
            f"/material/html/update/{self.material_html.id}/",
            self.material_html_update_data_invalid,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_material_html_not_exist(self):
        response = self.client.patch(
            "/material/html/update/3822/", self.material_html_update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteMaterialHTMLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="HTM",
            is_extra=True,
        )
        self.material_html = MaterialHTML.objects.create(
            material_id=self.material,
            content="Test markdown content",
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.client.force_authenticate(self.user)

    def test_material_html_delete_not_exist(self):
        response = self.client.delete(f"/material/html/delete/{self.material.id + 1}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_delete_correct(self):
        response = self.client.delete(f"/material/html/delete/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
