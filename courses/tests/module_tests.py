from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material

from accounts.models.user import User


class CreateModuleTestCase(TestCase):
    def setUp(self) -> None:
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

        self.module_data_correct = {
            "course_id": self.course.id,
            "name": "Test Module #",
        }
        self.module_data_blank = {}
        self.module_data_incorrect_types = {
            "course_id": "1",
            "name": 12,
        }

        self.url = reverse(viewname="create_module", current_app="courses")
        self.format = "json"
        self.client.force_authenticate(self.user)

    def test_create_module_correct(self):
        response = self.client.post(
            path=self.url, data=self.module_data_correct, format=self.format
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().name, "Test Module #")

    def test_create_module_blank(self):
        response = self.client.post(
            path=self.url, data=self.module_data_blank, format=self.format
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Module.objects.count(), 0)

    def test_create_module_incorrect_types(self):
        response = self.client.post(
            path=self.url, data=self.module_data_incorrect_types, format=self.format
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Module.objects.count(), 0)


class GetModuleTestCase(TestCase):
    def setUp(self) -> None:
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

        self.module_name = "Test Module #"
        self.module = Module.objects.create(
            course_id=self.course, name=self.module_name
        )
        self.view_name = "get_module_by_id"
        self.current_app = "courses"
        self.client.force_authenticate(self.user)

    def test_get_module_correct(self):
        response = self.client.get(
            path=reverse(
                viewname=self.view_name,
                args=[self.module.id],
                current_app=self.current_app,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.get().name, self.module_name)

    def test_get_module_not_found(self):
        response = self.client.get(
            path=reverse(
                viewname=self.view_name, args=[174], current_app=self.current_app
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateModuleTestCase(TestCase):
    def setUp(self) -> None:
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

        self.updated_module_name = "Updated Test Module"
        self.module = Module.objects.create(course_id=self.course, name="Test Module #")

        self.update_module_data_correct = {
            "name": self.updated_module_name,
        }
        self.update_module_data_incorrect_json = {
            "not_name": self.updated_module_name,
        }

        self.view_name = "update_module"
        self.current_app = "courses"
        self.client.force_authenticate(self.user)

    def test_update_module_correct(self):
        response = self.client.patch(
            path=reverse(
                viewname=self.view_name,
                args=[self.module.id],
                current_app=self.current_app,
            ),
            data=self.update_module_data_correct,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.get().name, self.updated_module_name)

    def test_update_module_not_found(self):
        response = self.client.patch(
            path=reverse(
                viewname=self.view_name, args=[986], current_app=self.current_app
            ),
            data=self.update_module_data_correct,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_module_incorrect_json(self):
        response = self.client.patch(
            path=reverse(
                viewname=self.view_name,
                args=[self.module.id],
                current_app=self.current_app,
            ),
            data=self.update_module_data_incorrect_json,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Module.objects.get().name, "Test Module #")


class DeleteModuleTestCase(TestCase):
    def setUp(self) -> None:
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

        self.module = Module.objects.create(course_id=self.course, name="Test Module #")

        self.view_name = "delete_module"
        self.current_app = "courses"
        self.client.force_authenticate(self.user)

    def test_delete_module_correct(self):
        response = self.client.delete(
            path=reverse(
                viewname=self.view_name,
                args=[self.module.id],
                current_app=self.current_app,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.count(), 0)

    def test_delete_module_not_found(self):
        response = self.client.delete(
            path=reverse(
                viewname=self.view_name, args=[1184], current_app=self.current_app
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Module.objects.get().name, "Test Module #")
        self.assertEqual(Module.objects.count(), 1)


class GetMaterialByModuleTestCase(TestCase):
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
        self.module_2 = Module.objects.create(
            course_id=self.course, name="Test module_2"
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material name",
            material_type="png",
            is_extra=True,
        )

        self.client.force_authenticate(self.user)

    def test_get_material_by_module_correct(self):
        response = self.client.get(f"/module/{self.module.id}/materials/")
        self.assertEqual(response.status_code, 200)

    def test_get_module_not_exist(self):
        response = self.client.get("/module/1223/materials/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_module(self):
        response = self.client.get(f"/module/{self.module_2.id}/materials/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# TODO: GetMaterialByModuleOrderTestCase


class UpdateMaterialOrderTestCase(TestCase):
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
        self.material_1 = Material.objects.create(
            module_id=self.module,
            name="Test material_1",
            material_type="png",
            is_extra=True,
        )
        self.material_2 = Material.objects.create(
            module_id=self.module,
            name="Test material_2",
            material_type="vio",
            is_extra=False,
        )

        self.new_order_data = {
            str(self.material_1.id): 1,
            str(self.material_2.id): 0,
        }

        self.invalid_order = {
            str(self.material_1.id): 10,
            str(self.material_2.id): 11,
        }

        self.client.force_authenticate(self.user)

    def test_update_module_not_exist(self):
        response = self.client.patch(
            f"/module/{self.module.id + 21}/materials/update_order/",
            self.new_order_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a module with that id"}
        )

    def test_update_invalid_order(self):
        response = self.client.patch(
            f"/module/{self.module.id}/materials/update_order/",
            self.invalid_order,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_correct(self):
        response = self.client.patch(
            f"/module/{self.module.id}/materials/update_order/",
            self.new_order_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
