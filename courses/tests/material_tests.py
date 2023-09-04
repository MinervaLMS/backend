from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material

from accounts.models.user import User


class CreateMaterialTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material_data = {
            "module_id": self.module.id,
            "name": "Image to reply",
            "material_type": "png",
            "is_extra": True,
        }

        self.material_invalid_types = {
            "module_id": 4,
            "name": "Papiro",
            "material_type": True,
            "is_extra": 2,
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self):
        response = self.client.post(
            "/material/create/", self.material_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_blank(self):
        response = self.client.post("/material/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_types(self):
        response = self.client.post(
            "/material/create/", self.material_invalid_types, format="json"
        )
        self.assertEqual(response.status_code, 400)


class GetMaterialTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material name",
            material_type="png",
            is_extra=True,
        )

        self.client.force_authenticate(self.user)

    def test_get_material_correct(self):
        response = self.client.get(f"/material/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_material_not_exist(self):
        response = self.client.get("/material/234/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateMaterialTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material name",
            material_type="png",
            is_extra=True,
        )

        self.material_update_data = {
            "name": "Test new name",
            "material_type": "new",
            "is_extra": False,
        }

        self.material_update_order = {"order": 23}

        self.material_invalid_fields = {"name": "Test new name", "last_name": "calipso"}

        self.client.force_authenticate(self.user)

    def test_update_material_not_exist(self):
        response = self.client.patch(
            "/material/update/2344/", self.material_update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with that id"}
        )

    def test_update_material_order(self):
        response = self.client.patch(
            f"/material/update/{self.material.id}/",
            self.material_update_order,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "You can not change the order of a material through this url"},
        )

    def test_update_material_order_incorrect(self):
        response = self.client.patch(
            f"/material/update/{self.material.id}/",
            self.material_invalid_fields,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "last_name attribute does not exist in material"},
        )

    def test_update_material_correct(self):
        response = self.client.patch(
            f"/material/update/{self.material.id}/",
            self.material_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMaterialTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material_1",
            material_type="png",
            is_extra=True,
        )

        self.client.force_authenticate(self.user)

    def test_material_delete_not_exist(self):
        response = self.client.delete(f"/material/delete/{self.material.id + 1}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_delete_correct(self):
        response = self.client.delete(f"/material/delete/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
