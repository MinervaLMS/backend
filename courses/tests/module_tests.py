from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models import *
from accounts.models import User


# TODO: CreateModuleTestCase


# TODO: GetModuleTestCase


# TODO: UpdateModuleTestCase


# TODO: DeleteModuleTestCase


class GetMaterialByModuleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email="test@example.com", password="testpassword", last_name="test_last_name", first_name="test_first_name")
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
        self.module_2 = Module.objects.create(
            course_id=self.course, name="Test module_2")
        self.material = Material.objects.create(
            module_id=self.module, name="Test material name", material_type="png", is_extra=True)

        self.client.force_authenticate(self.user)

    def test_get_material_by_module_correct(self):
        response = self.client.get(f'/module/{self.module.id}/materials/')
        self.assertEqual(response.status_code, 200)

    def test_get_module_not_exist(self):
        response = self.client.get('/module/1223/materials/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_module(self):
        response = self.client.get(f'/module/{self.module_2.id}/materials/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# TODO: GetMaterialByModuleOrderTestCase


class UpdateMaterialOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email="test@example.com", password="testpassword", last_name="test_last_name", first_name="test_first_name")
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
        self.material_1 = Material.objects.create(
            module_id=self.module, name="Test material_1", material_type="png", is_extra=True)
        self.material_2 = Material.objects.create(
            module_id=self.module, name="Test material_2", material_type="vio", is_extra=False)

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
            f'/module/{self.module.id+21}/materials/update_order/', self.new_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(loads(response.content), {
                         "message": "There is not a module with that id"})

    def test_update_invalid_order(self):
        response = self.client.patch(
            f'/module/{self.module.id}/materials/update_order/', self.invalid_order, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_correct(self):
        response = self.client.patch(
            f'/module/{self.module.id}/materials/update_order/', self.new_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
