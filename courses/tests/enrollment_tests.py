from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient

from ..models.course import Course
from ..models.enrollment import Enrollment
from accounts.models.user import User


class AppraiseCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.course1 = Course.objects.create(
            name="Test Course 1",
            alias="ED20241",
            description="This is a test course.",
            course_instructional_materials=0,
            course_assessment_materials=0,
            course_extra_materials=0,
            min_assessment_progress=80,
            average_stars=0,
            appraisals=0,
            comments=0,
        )

        self.course2 = Course.objects.create(
            name="Test Course 2",
            alias="test2",
            description="This is a test course.",
            course_instructional_materials=0,
            course_assessment_materials=0,
            course_extra_materials=0,
            min_assessment_progress=80,
            average_stars=0,
            appraisals=0,
            comments=0,
        )

        self.user1 = User.objects.create(
            email="test1@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User1",
        )

        self.user2 = User.objects.create(
            email="test2@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User2",
        )

        self.enrollment1 = Enrollment.objects.get(
            user_id=self.user1, course_id=self.course1
        )
        self.enrollment1.completion_date = timezone.now()
        self.enrollment1.save()

    def test_course_not_found(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            "/course/error/appraise/",
            {"stars": 10, "comment": "This is a test comment"},
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "message": "Course not found",
            },
        )

    def test_missing_fields(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            f"/course/{self.course1.alias}/appraise/",
            {
                "stars": 10,
                # missing comment
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "comment": "This field is required",
            },
        )

    def test_stars_out_of_range(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            f"/course/{self.course1.alias}/appraise/",
            {
                "stars": 11,
                "comment": "This is a test comment",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "stars": "Stars must be between 0 and 10",
            },
        )

    def test_user_not_enrolled(self):
        self.client.force_authenticate(self.user2)
        response = self.client.post(
            f"/course/{self.course2.alias}/appraise/",
            {
                "stars": 10,
                "comment": "This is a test comment",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "message": "You are not enrolled in this course",
            },
        )

    def test_user_not_finished_course(self):
        self.client.force_authenticate(self.user1)

        enrollment2 = Enrollment.objects.create(
            user_id=self.user1, course_id=self.course2
        )
        enrollment2.save()

        response = self.client.post(
            f"/course/{self.course2.alias}/appraise/",
            {
                "stars": 10,
                "comment": "This is a test comment",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "message": "You have not finished this course",
            },
        )

    def test_update_appraise_course(self):
        self.client.force_authenticate(self.user1)
        self.client.post(
            f"/course/{self.course1.alias}/appraise/",
            {
                "stars": 10,
                "comment": "This is a test comment",
            },
            format="json",
        )
        response2 = self.client.post(
            f"/course/{self.course1.alias}/appraise/",
            {
                "stars": 10,
                "comment": "This is a test comment",
            },
            format="json",
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            response2.json(),
            {
                "message": "Course appraised updated successfully",
            },
        )

    def test_create_appraise_course(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            f"/course/{self.course1.alias}/appraise/",
            {
                "stars": 10,
                "comment": "This is a test comment",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "Course appraised successfully",
            },
        )
