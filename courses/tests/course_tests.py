from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models import *
from accounts.models import User


class CreateCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.course_data = {
            'name': 'Test Course1',
            'alias': 'test',
            'description': 'This is a test course.'
        }

    def test_create_course_correct(self):
        response = self.client.post(
            '/course/create/', self.course_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_course_invalid_data(self):
        invalid_data = {
            'name': '',  # Invalid name
            'alias': 'test',
            'description': 'This is a test course.'
        }
        response = self.client.post(
            '/course/create/', invalid_data, format='json')
        self.assertEqual(response.status_code, 400)


class GetCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.course_data = {
            'name': 'Test Course1',
            'alias': 'test',
            'description': 'This is a test course.'
        }

    def test_get_course_correct(self):
        course = Course.objects.create(
            name='Test Course2', alias='test2', description='This is a test course.')
        response = self.client.get(f'/course/{course.alias}/')
        self.assertEqual(response.status_code, 200)

    def test_get_course_not_found(self):
        response = self.client.get('/course/nonexistent-course/')
        self.assertEqual(response.status_code, 404)


class UpdateCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.course_data = {
            'name': 'Test Course1',
            'alias': 'test',
            'description': 'This is a test course.'
        }

    def test_update_course_correct(self):
        course = Course.objects.create(
            name='Test Course2', alias='test2', description='This is a test course.')
        updated_data = {'name': 'Updated Course'}
        response = self.client.patch(
            f'/course/update/{course.alias}/', updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        course.refresh_from_db()
        self.assertEqual(course.name, 'Updated Course')

    def test_update_course_not_found(self):
        response = self.client.patch(
            '/course/update/nonexistent-course/', {}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_update_course_invalid_data(self):
        course = Course.objects.create(
            name='Test Course2', alias='test2', description='This is a test course.')
        invalid_data = {
            'name': '',  # Invalid name
        }
        response = self.client.patch(
            f'/course/update/{course.alias}/', invalid_data, format='json')
        self.assertEqual(response.status_code, 400)


class DeleteCourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course")
        self.user = User.objects.create(
            email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.course_data = {
            'name': 'Test Course1',
            'alias': 'test',
            'description': 'This is a test course.'
        }

    def test_delete_course_correct(self):
        course = Course.objects.create(
            name='Test Course2', alias='test2', description='This is a test course.')
        response = self.client.delete(f'/course/delete/{course.alias}/')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Course.DoesNotExist):
            course.refresh_from_db()

    def test_delete_course_not_found(self):
        response = self.client.delete('/course/delete/nonexistent-course/')
        self.assertEqual(response.status_code, 404)


# class GetModulesByCourseTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.course = Course.objects.create(
#             name="Test Course", alias="ED20241", description="This is a test course")
#         self.user = User.objects.create(
#             email='test@example.com', password='testpassword')
#         self.client.force_authenticate(self.user)
#         self.course_data = {
#             'name': 'Test Course',
#             'alias': 'test-course',
#             'description': 'This is a test course.'
#         }


# class GetModuleByCourseOrderTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.course = Course.objects.create(
#             name="Test Course", alias="ED20241", description="This is a test course")
#         self.user = User.objects.create(
#             email='test@example.com', password='testpassword')
#         self.client.force_authenticate(self.user)
#         self.course_data = {
#             'name': 'Test Course',
#             'alias': 'test-course',
#             'description': 'This is a test course.'
#         }


# class UpdateModuleOrderTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.course = Course.objects.create(
#             name="Test Course", alias="ED20241", description="This is a test course")
#         self.user = User.objects.create(
#             email='test@example.com', password='testpassword')
#         self.client.force_authenticate(self.user)
#         self.course_data = {
#             'name': 'Test Course',
#             'alias': 'test-course',
#             'description': 'This is a test course.'
#         }
