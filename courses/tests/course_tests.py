from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.instructor import Instructor

from institutions.models.institution import Institution
from accounts.models.user import User


class CreateCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution = Institution.objects.create(
            name="Institucion de Test",
            alias="IT",
            description="Institucion de Test",
            url="https://www.instituciontest.com",
        )
        self.course_data = {
            "institution": self.institution.id,
            "name": "Test Course 1",
            "alias": "test",
            "description": "This is a test course.",
        }

    def test_create_course_correct(self):
        response = self.client.post("/course/create/", self.course_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_course_invalid_data(self):
        invalid_data = {
            "institution": self.institution.id,
            "name": "",  # Invalid name
            "alias": "test",
            "description": "This is a test course.",
        }
        response = self.client.post("/course/create/", invalid_data, format="json")
        self.assertEqual(response.status_code, 400)


class GetCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution = Institution.objects.create(
            name="Institucion de Test",
            alias="IT",
            description="Institucion de Test",
            url="https://www.instituciontest.com",
        )

    def test_get_course_correct(self):

        user2 = User.objects.create(
            email="test2@example.com",
            password="testpassword2",
            first_name="Test2",
            last_name="User2",
        )
        course = Course.objects.create(
            institution=self.institution,
            name="Test Course2",
            alias="test2",
            description="This is a test course.",
        )
        instructor1 = Instructor.objects.create(
            user_id=self.user,
            course_id=course,
            instructor_type="T"
        )
        instructor2 = Instructor.objects.create(
            user_id=user2,
            course_id=course,
            instructor_type="A"
        )
        response = self.client.get(f"/course/{course.alias}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['institution']['id'], self.institution.id)
        self.assertEqual(response.json()['instructors'][0]['user_id'], self.user.id)
        self.assertEqual(response.json()['instructors'][1]['user_id'], user2.id)

    def test_get_course_not_found(self):
        response = self.client.get("/course/nonexistent-course/")
        self.assertEqual(response.status_code, 404)


class UpdateCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution = Institution.objects.create(
            name="Institucion de Test",
            alias="IT",
            description="Institucion de Test",
            url="https://www.instituciontest.com",
        )

    def test_update_course_correct(self):
        course = Course.objects.create(
            name="Test Course2",
            alias="test2",
            description="This is a test course.",
            institution=self.institution,
        )
        updated_data = {"name": "Updated Course"}
        response = self.client.patch(
            f"/course/update/{course.alias}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        course.refresh_from_db()
        self.assertEqual(course.name, "Updated Course")

    def test_update_course_not_found(self):
        response = self.client.patch(
            "/course/update/nonexistent-course/", {}, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_course_invalid_data(self):
        course = Course.objects.create(
            name="Test Course2",
            alias="test2",
            description="This is a test course.",
            institution=self.institution,
        )
        invalid_data = {
            "name": "",  # Invalid name
            "alias": "test",
            "description": "This is a test course.",
        }
        response = self.client.patch(
            f"/course/update/{course.alias}/", invalid_data, format="json"
        )
        self.assertEqual(response.status_code, 400)


class DeleteCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution = Institution.objects.create(
            name="Institucion de Test",
            alias="IT",
            description="Institucion de Test",
            url="https://www.instituciontest.com",
        )

    def test_delete_course_correct(self):
        course = Course.objects.create(
            name="Test Course 2",
            alias="test2",
            description="This is a test course.",
            institution=self.institution,
        )
        response = self.client.delete(f"/course/delete/{course.alias}/")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Course.DoesNotExist):
            course.refresh_from_db()

    def test_delete_course_not_found(self):
        response = self.client.delete("/course/delete/nonexistent-course/")
        self.assertEqual(response.status_code, 404)


class GetModulesByCourseTestCase(TestCase):
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
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_get_modules_by_course_not_exist(self):
        response = self.client.get("/course/nonexistent-course/modules/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a course with that id"}
        )

    def test_get_modules_by_course_empty(self):
        response = self.client.get(f"/course/{self.course.alias}/modules/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There are not modules in this course"}
        )

    def test_get_modules_by_course_correct(self):
        module = Module.objects.create(course_id=self.course, name="Test module")
        response = self.client.get(f"/course/{self.course.alias}/modules/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            [
                {
                    "id": module.id,
                    "course_id": self.course.id,
                    "name": module.name,
                    "order": module.order,
                }
            ],
        )


class GetModuleByCourseOrderTestCase(TestCase):
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
            email="test@example.com", password="testpassword"
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.client.force_authenticate(self.user)

    def test_get_module_by_course_order_not_exist(self):
        response = self.client.get("/course/nonexistent-course/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a course with that id"}
        )

    def test_get_module_by_course_order_invalid(self):
        response = self.client.get(f"/course/{self.course.alias}/10/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There are not modules by this order"}
        )

    def test_get_modules_by_course_order_correct(self):
        response = self.client.get(f"/course/{self.course.alias}/{self.module.order}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            {
                "id": self.module.id,
                "course_id": self.course.id,
                "name": self.module.name,
                "order": self.module.order,
            },
        )


class UpdateModuleOrderTestCase(TestCase):
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
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_update_module_order_not_exist(self):
        response = self.client.patch(
            "/course/nonexistent-course/modules/update_order/", {}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a course with that id"}
        )

    def test_update_module_order_invalid(self):
        invalid_order = {
            "module1_id": 2,
            "module2_id": 4,
        }
        response = self.client.patch(
            f"/course/{self.course.alias}/modules/update_order/",
            invalid_order,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content), {"message": "This modules order is not valid"}
        )

    def test_update_module_order_correct(self):
        module_1 = Module.objects.create(course_id=self.course, name="Test module 1")
        module_2 = Module.objects.create(course_id=self.course, name="Test module 2")
        new_order = {
            str(module_1.id): 1,
            str(module_2.id): 0,
        }
        response = self.client.patch(
            f"/course/{self.course.alias}/modules/update_order/",
            new_order,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            [
                {
                    "id": module_1.id,
                    "name": module_1.name,
                    "order": 1,
                    "course_id": self.course.id,
                },
                {
                    "id": module_2.id,
                    "name": module_2.name,
                    "order": 0,
                    "course_id": self.course.id,
                },
            ],
        )
