from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from courses.models.material import Material
from courses.models.course import Course
from accounts.models.user import User
from courses.models.module import Module
from institutions.models.institution import Institution
from ..models.io_code_submission import IoCodeSubmission


class CreateIoCodeSubmissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.institution = Institution.objects.create(
            name="Test Institution",
            alias="TestInstitution",
            description="This is a test institution",
        )
        self.course = Course.objects.create(
            name="Test Course",
            alias="TestCourse",
            description="This is a test course",
            institution=self.institution,
        )

        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="I",
            is_extra=False,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="JHuyfub434eknjbv",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.io_code_submission_data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "response_char": "A",
            "execution_time": 1,
            "execution_memory": 1,
            "completion_rate": 1.0,
        }

        self.io_code_submission_data_invalid = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "response_char": "A",
            "execution_time": "uno",
            "execution_memory": "uno",
            "completion_rate": 1.0,
        }

        self.io_code_submission_data_no_material = {
            "material_id": self.material.id + 1,
            "user_id": self.user.id,
            "response_char": "A",
            "execution_time": 1,
            "execution_memory": 1,
            "completion_rate": 1.0,
        }

        self.io_code_submission_data_no_user = {
            "material_id": self.material.id,
            "user_id": self.user.id + 1,
            "response_char": "A",
            "execution_time": 1,
            "execution_memory": 1,
            "completion_rate": 1.0,
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self):
        response = self.client.post(
            "/iocode/submission/create/", self.io_code_submission_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_blank(self):
        response = self.client.post("/iocode/submission/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_no_material(self):
        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_no_material,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_no_user(self):
        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_no_user,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_types(self):
        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_invalid,
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class GetIoCodeSubmissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.institution = Institution.objects.create(
            name="Test Institution",
            alias="TestInstitution",
            description="This is a test institution",
        )
        self.course = Course.objects.create(
            name="Test Course",
            alias="TestCourse",
            description="This is a test course",
            institution=self.institution,
        )

        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="I",
            is_extra=False,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="JHuyfub434eknjbv",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.io_code_submission = IoCodeSubmission.objects.create(
            material_id=self.material,
            user_id=self.user,
            response_char="A",
            execution_time=1,
            execution_memory=1,
            completion_rate=1.0,
        )

        self.client.force_authenticate(self.user)

    def test_get_incorrect(self):
        response = self.client.get(
            f"/iocode/submission/{(self.io_code_submission.submission_id)+1}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_correct(self):
        response = self.client.get(
            f"/iocode/submission/{self.io_code_submission.submission_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteIoCodeSubmissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(
            name="Test Institution",
            alias="TestInstitution",
            description="This is a test institution",
        )
        self.course = Course.objects.create(
            institution=self.institution,
            name="Test Course",
            alias="TestCourse",
            description="This is a test course",
        )

        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="I",
            is_extra=False,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="JHuyfub434eknjbv",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.io_code_submission = IoCodeSubmission.objects.create(
            material_id=self.material,
            user_id=self.user,
            response_char="A",
            execution_time=1,
            execution_memory=1,
            completion_rate=1.0,
        )

        self.client.force_authenticate(self.user)

    def test_delete_incorrect(self):
        response = self.client.delete(
            f"/iocode/submission/delete/{(self.io_code_submission.submission_id)+1}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_correct(self):
        response = self.client.delete(
            f"/iocode/submission/delete/{self.io_code_submission.submission_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateIoCodeSubmissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.institution = Institution.objects.create(
            name="Test Institution",
            alias="TestInstitution",
            description="This is a test institution",
        )

        self.course = Course.objects.create(
            institution=self.institution,
            name="Test Course",
            alias="TestCourse",
            description="This is a test course",
        )

        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="I",
            is_extra=False,
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="JHuyfub434eknjbv",
            last_name="test_last_name",
            first_name="test_first_name",
        )

        self.io_code_submission = IoCodeSubmission.objects.create(
            material_id=self.material,
            user_id=self.user,
            response_char="A",
            execution_time=1,
            execution_memory=1,
            completion_rate=1.0,
        )

        self.client.force_authenticate(self.user)

        self.io_code_submission_data_update_response_char = {
            "response_char": "W",
        }

        self.io_code_submission_data_update_execution_time = {
            "execution_time": 2,
        }

        self.io_code_submission_data_update_both = {
            "response_char": "W",
            "execution_time": 2,
        }

    def test_update_incorrect(self):
        response = self.client.patch(
            f"/iocode/submission/update/{(self.io_code_submission.submission_id)+1}/",
            self.io_code_submission_data_update_response_char,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_blank(self):
        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_submission_id_blank(self):
        response = self.client.patch("/iocode/submission/update//", {}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_update_response_char(self):
        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_response_char,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_execution_time(self):
        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_execution_time,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_both(self):
        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_both,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
