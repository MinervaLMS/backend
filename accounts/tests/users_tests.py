from django.test import TestCase
from rest_framework.test import APIClient

from courses.models import Module, Material
from ..models.user import User
from courses.models.course import Course
from institutions.models.institution import Institution
from json import loads
from courses.helpers.create_all_accesses import create_accesses_for_material


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


class GetUserMaterialsTestCase(TestCase):
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
        # Create all accesses for the material created
        create_accesses_for_material(course_id=self.course.id, material=self.material)

        self.client.force_authenticate(self.user)

    def test_get_user_materials_correct(self):
        response = self.client.get(
            f"/users/{self.user.id}/module/{self.module.id}/materials/"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user_materials_no_materials(self):
        response = self.client.get(f"/users/{self.user.id}/module/10000/materials/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            loads(response.content),
            {"message": "There are not materials in this module"},
        )

    def test_get_user_materials_user_nonexistent(self):
        response = self.client.get(
            f"/users/{self.user.id+1000}/module/10000/materials/"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a user with that id"},
        )
