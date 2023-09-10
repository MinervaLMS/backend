from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material
from ..models.module_progress import Module_progress
from accounts.models.user import User
from institutions.models.institution import Institution


class CreateModuleProgressTestCase(TestCase):
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
        self.module_progress = {
            "user_id": self.user.id,
            "module_id": self.module.id,
        }
        self.module_progress_incorrect = {
            "user_id": self.user.id,
            "module_id": 100,
        }
        self.client.force_authenticate(self.user)

    def test_create_module_progress_correct(self):
        response = self.client.post(
            path="/module_progress/create/", data=self.module_progress, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_module_progress_incorrect(self):
        response = self.client.post(
            path="/module_progress/create/",
            data=self.module_progress_incorrect,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetModuleProgressTestCase(TestCase):
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
        # Instructional material
        self.material_1 = {
            "module_id": self.module.id,
            "name": "Test material_1",
            "material_type": "png",
            "is_extra": False,
        }
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
        self.material_4 = {
            "module_id": self.module.id,
            "name": "Test material_4",
            "material_type": "ioc",
            "is_extra": False,
        }
        self.module_progress = Module_progress.objects.create(
            user_id=self.user, module_id=self.module
        )
        self.client.force_authenticate(self.user)
    # Normal add

    def test_1get_add_count_progress_instructional(self):
        self.client.post(
            path="/material/create/", data=self.material_1, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_2, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 50)
        self.assertEqual(content["module_assessment_progress"], 0)

    def test_2get_add_count_progress_assessment(self):
        self.client.post(
            path="/material/create/", data=self.material_3, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_4, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 0)
        self.assertEqual(content["module_assessment_progress"], 50)
    # Add if it gets above the max

    def test_3get_addMax_count_progress_instructional(self):
        self.client.post(
            path="/material/create/", data=self.material_1, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_2, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 100)
        self.assertEqual(content["module_assessment_progress"], 0)

    def test_4get_addMax_count_progress_assessment(self):
        self.client.post(
            path="/material/create/", data=self.material_3, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_4, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 0)
        self.assertEqual(content["module_assessment_progress"], 100)
    # Incorrect format

    def test_5get_add_incorrect_count_progress_instructional_assessment(self):
        self.client.post(
            path="/material/create/", data=self.material_1, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_2, format="json"
        )
        response = self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "Peje", "type": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    # Normal subtract

    def test_6get_subtract_count_progress_instructional(self):
        self.client.post(
            path="/material/create/", data=self.material_1, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_2, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": False},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 50)
        self.assertEqual(content["module_assessment_progress"], 0)

    def test_7get_subtract_count_progress_assessment(self):
        self.client.post(
            path="/material/create/", data=self.material_3, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_4, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": False},
            format="json",
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 0)
        self.assertEqual(content["module_assessment_progress"], 50)

    # Delete material
    def test_8get_delete_count_progress_instructional(self):
        self.client.post(
            path="/material/create/", data=self.material_1, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_2, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "instructional", "type": True},
            format="json",
        )
        self.client.delete(
            path="/material/delete/16/"
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 100)
        self.assertEqual(content["module_assessment_progress"], 0)

    def test_9get_delete_count_progress_assessment(self):
        self.client.post(
            path="/material/create/", data=self.material_3, format="json"
        )
        self.client.post(
            path="/material/create/", data=self.material_4, format="json"
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.patch(
            path=f"/module_progress/update/{self.user.id}/{self.module.id}/",
            data={"material_type": "assessment", "type": True},
            format="json",
        )
        self.client.delete(
            path="/material/delete/18/"
        )
        response = self.client.get(
            path=f"/module_progress/{self.user.id}/{self.module.id}/"
        )
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["module_instructional_progress"], 0)
        self.assertEqual(content["module_assessment_progress"], 100)
