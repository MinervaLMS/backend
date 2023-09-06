from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from courses.models.material import Material
from ..models.material_io_code import MaterialIoCode
from courses.models.course import Course
from accounts.models.user import User
from courses.models.module import Module


class CreateMaterialIoCodeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="IOC",
            is_extra=False,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.material_iocode_data = {
            "material_id": self.material.id,
            "max_time": 18,
            "max_memory": 2,
        }

        self.material_iocode_no_material_data = {
            "material_id": self.material.id + 1,
            "max_time": 100,
            "max_memory": 1,
        }

        self.material_iocode_data_invalid = {
            "material_id": True,
            "max_time": "String in Integer Field",
            "max_memory": "String in Integer Field"
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self):
        response = self.client.post(
            "/material/iocode/create/", self.material_iocode_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_blank(self):
        response = self.client.post("/material/iocode/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_no_material(self):
        response = self.client.post(
            "/material/iocode/create/", self.material_iocode_no_material_data, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_repeat(self):
        self.client.post(
            "/material/iocode/create/", self.material_iocode_data, format="json"
        )
        response2 = self.client.post(
            "/material/iocode/create/", self.material_iocode_data, format="json"
        )
        self.assertEqual(response2.status_code, 400)

    def test_create_invalid_types(self):
        response = self.client.post(
            "/material/iocode/create/", self.material_iocode_data_invalid, format="json"
        )
        self.assertEqual(response.status_code, 400)

class GetMaterialIoCodeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="IOC",
            is_extra=False,
        )
        
        self.material_iocode = MaterialIoCode.objects.create(
            material_id=self.material,
            max_time=18,
            max_memory=2
        )
        
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.client.force_authenticate(self.user)

    def test_get_material_iocode_correct(self):
        response = self.client.get(f"/material/iocode/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_material_iocode_not_exist(self):
        response = self.client.get("/material/1122/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateMaterialIoCodeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="IOC",
            is_extra=False,
        )
        
        self.material_iocode = MaterialIoCode.objects.create(
            material_id=self.material,
            max_time=18,
            max_memory=2
        )
        
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        
        self.material_iocode_update_data = {
            "max_time": 19,
            "max_memory": 7
        }

        self.material_iocode_update_data_invalid = {
            "material_id": 999,
        }

        self.client.force_authenticate(self.user)

    def test_update_material_iocode_correct(self):
        response = self.client.patch(
            f"/material/iocode/update/{self.material.id}/",
            self.material_iocode_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_material_iocode_blank(self):
        response = self.client.patch(
            f"/material/iocode/update/{self.material.id}/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_material_iocode_invalid(self):
        response = self.client.patch(
            f"/material/iocode/update/{self.material_iocode.id}/",
            self.material_iocode_update_data_invalid,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_material_iocode_not_exist(self):
        response = self.client.patch(
            "/material/iocode/update/3822/", self.material_iocode_update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class DeleteMaterialIoCodeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="IOC",
            is_extra=False,
        )
        
        self.material_iocode = MaterialIoCode.objects.create(
            material_id=self.material,
            max_time=18,
            max_memory=2
        )
        
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.client.force_authenticate(self.user)

    def test_material_iocode_delete_not_exist(self):
        response = self.client.delete(f"/material/iocode/delete/{self.material.id + 1}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_delete_correct(self):
        response = self.client.delete(f"/material/iocode/delete/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)