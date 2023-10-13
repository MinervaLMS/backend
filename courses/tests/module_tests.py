from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material

from accounts.models.user import User
from institutions.models.institution import Institution


class CreateModuleTestCase(TestCase):
    def setUp(self) -> None:
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

        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.updated_module_name = "Updated Test Module"
        self.module = Module.objects.create(
            course_id=self.course, name="Test Module #")

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

        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.module = Module.objects.create(
            course_id=self.course, name="Test Module #")

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
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
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
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
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
            loads(response.content), {
                "message": "There is not a module with that id"}
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

# TODO : CreateMaterialTestCase


class CreateMaterialTestCase(TestCase):
    def setUp(self) -> None:
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

        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
        # Extra material
        self.material_1 = {
            "module_id": self.module.id,
            "name": "Test material_1",
            "material_type": "png",
            "is_extra": True,
        }

        # Instructional material
        self.material_2 = {
            "module_id": self.module.id,
            "name": "Test material_2",
            "material_type": "png",
            "is_extra": False,
        }
        # Assessment material
        self.material_3 = {
            "module_id": self.module.id,
            "name": "Test material_3",
            "material_type": "ioc",
            "is_extra": False,
        }
        self.client.force_authenticate(self.user)

    def test_get_count_extra_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_1, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 1)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 0)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)

    def test_get_count_instructional_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_2, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 1)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)

    def test_get_count_assessment_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_3, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 0)
        self.assertEqual(Module.objects.get().module_assessment_materials, 1)

# TODO : CreateMaterialTestCase


class DeleteMaterialTestCase(TestCase):
    def setUp(self) -> None:
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

        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
        # Extra material
        self.material_1 = {
            "module_id": self.module.id,
            "name": "Test material_1",
            "material_type": "png",
            "is_extra": True,
        }

        # Instructional material
        self.material_2 = {
            "module_id": self.module.id,
            "name": "Test material_2",
            "material_type": "png",
            "is_extra": False,
        }
        # Assessment material
        self.material_3 = {
            "module_id": self.module.id,
            "name": "Test material_3",
            "material_type": "ioc",
            "is_extra": False,
        }
        self.client.force_authenticate(self.user)

    def test_1get_count_extra_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_1, format="json"
        )
        response2 = self.client.post(
            "/material/create/", self.material_2, format="json"
        )
        response3 = self.client.post(
            "/material/create/", self.material_3, format="json"
        )
        response4 = self.client.delete(
            "/material/delete/4/"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(response3.status_code, 201)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 2)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 1)
        self.assertEqual(Module.objects.get().module_assessment_materials, 1)

    def test_2get_count_instructional_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_1, format="json"
        )
        response2 = self.client.post(
            "/material/create/", self.material_2, format="json"
        )
        response3 = self.client.post(
            "/material/create/", self.material_3, format="json"
        )
        response4 = self.client.delete(
            "/material/delete/8/"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(response3.status_code, 201)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 2)
        self.assertEqual(Module.objects.get().module_extra_materials, 1)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 0)
        self.assertEqual(Module.objects.get().module_assessment_materials, 1)

    def test_3get_count_assessment_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_1, format="json"
        )
        response2 = self.client.post(
            "/material/create/", self.material_2, format="json"
        )
        response3 = self.client.post(
            "/material/create/", self.material_3, format="json"
        )
        response4 = self.client.delete(
            "/material/delete/12/"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(response3.status_code, 201)
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 2)
        self.assertEqual(Module.objects.get().module_extra_materials, 1)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 1)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)

# TODO: UpdateMaterialTestCase


class UpdateMaterialTestCase(TestCase):
    def setUp(self) -> None:
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

        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(
            course_id=self.course, name="Test module")
        # Extra material
        self.material_1 = {
            "module_id": self.module.id,
            "name": "Test material_1",
            "material_type": "png",
            "is_extra": True,
        }
        self.material_update_1 = {
            "name": "Test material_1",
            "material_type": "png",
            "is_extra": False,
        }
        # Instructional material
        self.material_2 = {
            "module_id": self.module.id,
            "name": "Test material_2",
            "material_type": "png",
            "is_extra": False,
        }
        self.material_update_2 = {
            "name": "Test material_2",
            "material_type": "ioc",
            "is_extra": False,
        }
        # Assessment material
        self.material_3 = {
            "module_id": self.module.id,
            "name": "Test material_3",
            "material_type": "ioc",
            "is_extra": False,
        }
        self.material_update_3 = {
            "name": "Test material_3",
            "material_type": "png",
            "is_extra": False,
        }
        self.client.force_authenticate(self.user)

    def test_1get_count_update_extra_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_1, format="json"
        )
        response2 = self.client.patch(
            "/material/update/22/", self.material_update_1, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 1)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)

    def test_2get_count_update_instructional_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_2, format="json"
        )
        response2 = self.client.patch(
            "/material/update/23/", self.material_update_2, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 1)
        self.assertEqual(Module.objects.get().module_assessment_materials, 0)

    def test_3get_count_update_assessment_material_correct(self):
        response = self.client.post(
            "/material/create/", self.material_3, format="json"
        )
        response2 = self.client.patch(
            "/material/update/24/", self.material_update_3, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Module.objects.get().module_total_materials, 1)
        self.assertEqual(Module.objects.get().module_extra_materials, 0)
        self.assertEqual(Module.objects.get(
        ).module_instructional_materials, 0)
        self.assertEqual(Module.objects.get().module_assessment_materials, 1)
