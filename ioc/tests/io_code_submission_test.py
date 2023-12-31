"""Module for testing the IoCodeSubmission model and its endpoints."""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from unittest.mock import patch
from courses.models.material import Material
from courses.models.course import Course
from accounts.models.user import User
from courses.models.module import Module
from institutions.models.institution import Institution
from ioc.models.material_io_code import MaterialIoCode
from ..models.io_code_submission import IoCodeSubmission


class CreateIoCodeSubmissionTestCase(TestCase):
    """Class that tests the creation of a IoCodeSubmission instance."""

    def setUp(self) -> None:
        """Method that sets up the client and the data to be used in the tests."""

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
            material_type="IOC",
            is_extra=False,
        )
        self.material_other = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="PDF",
            is_extra=False,
        )
        self.material_ioc = MaterialIoCode.objects.create(
            material_id=self.material,
            max_time=1000,
            max_memory=1000,
        )
        self.material_ioc_other = MaterialIoCode.objects.create(
            material_id=self.material_other,
            max_time=1000,
            max_memory=1000,
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
            "code": "print('Hello World')",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_non_ioc = {
            "material_id": self.material_other.id,
            "user_id": self.user.id,
            "code": "print('Hello World')",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_wrong_material_id = {
            "material_id": 999,
            "user_id": self.user.id,
            "code": "print('Hello World')",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_wrong_answer = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "code": "print()",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_copilation_error = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "code": "while",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_memeory_exceed = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "code": "while(True):\n    pass",
            "execution_time": 1000,
            "execution_memory": 1000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_time_exceed = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "code": "while(True):\n    pass",
            "execution_time": 10,
            "execution_memory": 10000,
            "completion_rate": 1.0,
            "language": "py",
        }

        self.io_code_submission_data_invalid = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "execution_time": "uno",
            "execution_memory": "uno",
            "completion_rate": 1.0,
        }

        self.io_code_submission_data_no_material = {
            "material_id": self.material.id + 2,
            "user_id": self.user.id,
            "execution_time": 1,
            "execution_memory": 1,
            "completion_rate": 1.0,
        }

        self.io_code_submission_data_no_user = {
            "material_id": self.material.id,
            "user_id": self.user.id + 1,
            "execution_time": 1,
            "execution_memory": 1,
            "completion_rate": 1.0,
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with correct data."""

        response = self.client.post(
            "/iocode/submission/create/", self.io_code_submission_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_non_ioc_material(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with a material with non ioc material_type."""

        response = self.client.post(
            "/iocode/submission/create/", self.io_code_submission_data_non_ioc, format="json"
        )
        self.assertEqual(response.json()['message'], "Material type is not IOC")

    def test_create_wrong_material_id(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with wrong material_id"""

        response = self.client.post(
            "/iocode/submission/create/", self.io_code_submission_wrong_material_id, format="json"
        )
        self.assertEqual(response.json()['message'], "No material found related to given material_id")

    def test_create_blank(self) -> None:
        """Method that tests the creation of a IoCodeSubmission
        instance with blank data."""

        response = self.client.post("/iocode/submission/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_no_material(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with no material."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_no_material,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_no_user(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with no user."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_no_user,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_types(self) -> None:
        """Method that tests the creation of a IoCodeSubmission instance
        with invalid types."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_invalid,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    @patch(
        "ioc.serializers.io_code_submission_serializer.judge",
        return_value=(
            {
                "max_memory": 8960,
                "max_time": 0.03,
                "submission_id": 72,
                "verdict": {"message": "Accepted", "verdict": "AC"},
            },
            201,
        ),
    )
    def test_submission_judge_correct_answer(self, mock_judge) -> None:
        """Method that checks if the IoCodeSubmission instance,
        with a correct code is successfully submitted and judged
        at the judge's URL."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        submission = IoCodeSubmission.objects.latest("submission_date")
        self.assertEqual(submission.response_char, "A")

    @patch(
        "ioc.serializers.io_code_submission_serializer.judge",
        return_value=(
            {
                "max_memory": 8960,
                "max_time": 0.03,
                "submission_id": 72,
                "verdict": {"message": "Wrong Answer", "verdict": "WA"},
                "wrong_case": 1,
            },
            201,
        ),
    )
    def test_submission_judge_wrong_answer(self, mock_judge) -> None:
        """Method that checks if the IoCodeSubmission instance,
        with a wrong code is successfully submitted and judged
        at the judge's URL."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_wrong_answer,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        submission = IoCodeSubmission.objects.latest("submission_date")
        self.assertEqual(submission.response_char, "W")

    @patch(
        "ioc.serializers.io_code_submission_serializer.judge",
        return_value=(
            {
                "max_memory": 8832,
                "max_time": 11.99,
                "submission_id": 72,
                "verdict": {"message": "Time Limit Exceeded", "verdict": "TLE"},
                "wrong_case": 1,
            },
            201,
        ),
    )
    def test_submission_judge_time_exceed(self, mock_judge) -> None:
        """Method that checks if the IoCodeSubmission instance,
        with a code that exceed the time limit is successfully submitted and judged
        at the judge's URL."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_time_exceed,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        submission = IoCodeSubmission.objects.latest("submission_date")
        self.assertEqual(submission.response_char, "T")

    @patch(
        "ioc.serializers.io_code_submission_serializer.judge",
        return_value=(
            {
                "max_memory": 7680,
                "max_time": 0.09,
                "submission_id": 72,
                "verdict": {"message": "Memory Limit Exceeded", "verdict": "MLE"},
                "wrong_case": 1,
            },
            201,
        ),
    )
    def test_submission_judge_memory_exceed(self, mock_judge) -> None:
        """Method that checks if the IoCodeSubmission instance,
        with a code that exceed the memory limit is successfully submitted and judged
        at the judge's URL."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_memeory_exceed,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        submission = IoCodeSubmission.objects.latest("submission_date")
        self.assertEqual(submission.response_char, "M")

    @patch(
        "ioc.serializers.io_code_submission_serializer.judge",
        return_value=(
            {
                "submission_id": 72,
                "verdict": """Judge execution: code compilation
                or problem_id don't exist.""",
            },
            201,
        ),
    )
    def test_submission_judge_copilation_error(self, mock_judge) -> None:
        """Method that checks if the IoCodeSubmission instance,
        with a code that does not compile is successfully submitted and judged
        at the judge's URL."""

        response = self.client.post(
            "/iocode/submission/create/",
            self.io_code_submission_data_copilation_error,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        submission = IoCodeSubmission.objects.latest("submission_date")
        self.assertEqual(submission.response_char, "C")


class GetIoCodeSubmissionTestCase(TestCase):
    """Class that tests the get method of the IoCodeSubmission model."""

    def setUp(self):
        """Method that sets up the client and the data to be used in the tests."""
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

    def test_get_incorrect(self) -> None:
        """Method that tests the get method of the IoCodeSubmission model
        with an incorrect id."""

        response = self.client.get(
            f"/iocode/submission/{(self.io_code_submission.submission_id)+1}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_correct(self) -> None:
        """Method that tests the get method of the IoCodeSubmission
        model with a correct id."""
        response = self.client.get(
            f"/iocode/submission/{self.io_code_submission.submission_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteIoCodeSubmissionTestCase(TestCase):
    """Class that tests the delete method of the IoCodeSubmission model."""

    def setUp(self) -> None:
        """Method that sets up the client and the data to be used in the tests."""

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

    def test_delete_incorrect(self) -> None:
        """Method that tests the delete method of the IoCodeSubmission
        model with an incorrect id."""

        response = self.client.delete(
            f"/iocode/submission/delete/{(self.io_code_submission.submission_id)+1}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_correct(self) -> None:
        """Method that tests the delete method of the IoCodeSubmission
        model with a correct id."""

        response = self.client.delete(
            f"/iocode/submission/delete/{self.io_code_submission.submission_id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateIoCodeSubmissionTestCase(TestCase):
    """Class that tests the update method of the IoCodeSubmission model."""

    def setUp(self) -> None:
        """Method that sets up the client and the data to be used in the tests."""

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

    def test_update_incorrect(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with an incorrect id."""

        response = self.client.patch(
            f"/iocode/submission/update/{(self.io_code_submission.submission_id)+1}/",
            self.io_code_submission_data_update_response_char,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_blank(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with blank data."""

        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_submission_id_blank(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with blank submission_id."""

        response = self.client.patch("/iocode/submission/update//", {}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_update_response_char(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with response_char."""

        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_response_char,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_execution_time(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with execution_time."""

        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_execution_time,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_both(self) -> None:
        """Method that tests the update method of the IoCodeSubmission
        model with both response_char and execution_time."""

        response = self.client.patch(
            f"/iocode/submission/update/{self.io_code_submission.submission_id}/",
            self.io_code_submission_data_update_both,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
