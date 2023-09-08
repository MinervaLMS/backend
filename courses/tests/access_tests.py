from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models import Access
from ..models.course import Course
from ..models.module import Module
from ..models.material import Material

from accounts.models.user import User
from institutions.models.institution import Institution


class CreateAccessTestCase(TestCase):
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
            course_id=self.course,
            name="Test module",
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="pdf",
        )
        self.access_data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
        }
        self.client.force_authenticate(self.user)

    def test_create_access_user_not_exist(self):
        data = {
            "material_id": self.material.id,
            "user_id": -100,
        }
        response = self.client.post("/access/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a user with this id"}
        )

    def test_create_access_materia_not_exist(self):
        data = {
            "material_id": -100,
            "user_id": self.user.id,
        }
        response = self.client.post("/access/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with this id"}
        )

    def test_create_access_user_not_enrolled(self):
        course_temp = Course.objects.create(
            name="Web Development",
            alias="WD",
            institution=self.institution,
        )
        module_temp = Module.objects.create(
            course_id=course_temp,
            name="Test module",
        )
        materia_temp = Material.objects.create(
            module_id=module_temp,
            name="Test material",
            material_type="pdf",
        )
        access_data = {
            "material_id": materia_temp.id,
            "user_id": self.user.id,
        }
        response = self.client.post("/access/create/", access_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {"message": "You do not have permission to access this material"},
        )

    def test_create_correct(self):
        response1 = self.client.post("/access/create/", self.access_data, format="json")
        response2 = self.client.post("/access/create/", self.access_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class GetAccessTestCase(TestCase):
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
            course_id=self.course,
            name="Test module",
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="pdf",
        )
        self.access = Access.objects.create(
            material_id=self.material,
            user_id=self.user,
        )

        self.client.force_authenticate(self.user)

    def test_get_access_nonexistent(self):
        response = self.client.get("/access/100/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not an access with that material and user"},
        )

    def test_get_access_correct(self):
        response = self.client.get(f"/access/{self.material.id}/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Access.objects.last().views, 1)


class UpdateAccessLikeTestCase(TestCase):
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
            course_id=self.course,
            name="Test module",
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="pdf",
        )

        self.client.force_authenticate(self.user)

    def test_update_access_user_not_exist(self):
        data = {
            "material_id": self.material.id,
            "user_id": -100,
        }
        response = self.client.patch("/access/update/like/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a user with this id"}
        )

    def test_update_access_materia_not_exist(self):
        data = {
            "material_id": -100,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/like/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with this id"}
        )

    def test_update_access_nonexistent(self):
        data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/like/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {"message": "You should access to the material before"},
        )

    def test_upadate_access_correct(self):
        Access.objects.create(
            material_id=self.material,
            user_id=self.user,
        )
        data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/like/", data, format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Access.objects.last().like, True)
        self.assertEqual(
            loads(response.content), {"message": "Access assessed successfully"}
        )


class UpdateAccessDislikeTestCase(TestCase):
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
            course_id=self.course,
            name="Test module",
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="pdf",
        )

        self.client.force_authenticate(self.user)

    def test_update_access_user_not_exist(self):
        data = {
            "material_id": self.material.id,
            "user_id": -100,
        }
        response = self.client.patch("/access/update/dislike/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a user with this id"}
        )

    def test_update_access_materia_not_exist(self):
        data = {
            "material_id": -100,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/dislike/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with this id"}
        )

    def test_update_access_nonexistent(self):
        data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/dislike/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {"message": "You should access to the material before"},
        )

    def test_upadate_access_correct(self):
        Access.objects.create(
            material_id=self.material,
            user_id=self.user,
        )
        data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
        }
        response = self.client.patch("/access/update/dislike/", data, format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Access.objects.last().like, False)
        self.assertEqual(
            loads(response.content), {"message": "Access assessed successfully"}
        )


class DeleteAccessTestCase(TestCase):
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
            course_id=self.course,
            name="Test module",
        )
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="pdf",
        )

        self.access = Access.objects.create(
            material_id=self.material,
            user_id=self.user,
        )

        self.client.force_authenticate(self.user)

    def test_delete_access_nonexistent(self):
        response = self.client.delete("/access/delete/100/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not an access with that material and user"},
        )

    def test_delete_access_correct(self):
        response = self.client.delete(
            f"/access/delete/{self.material.id}/{self.user.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Access.objects.count(), 0)
