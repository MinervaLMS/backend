from django.test import TestCase
from rest_framework.test import APIClient

from .models import Course
from accounts.models import User

class CourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)
        self.course_data = {
            'name': 'Test Course',
            'alias': 'test-course',
            'description': 'This is a test course.'
        }

    def test_create_course(self):
        response = self.client.post('/course/create/', self.course_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_course(self):
        course = Course.objects.create(name='Test Course', alias='test-course', description='This is a test course.')
        response = self.client.get(f'/course/get/{course.alias}/')
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        course = Course.objects.create(name='Test Course', alias='test-course', description='This is a test course.')
        updated_data = {'name': 'Updated Course'}
        response = self.client.patch(f'/course/update/{course.alias}/', updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        course.refresh_from_db()
        self.assertEqual(course.name, 'Updated Course')

    def test_delete_course(self):
        course = Course.objects.create(name='Test Course', alias='test-course', description='This is a test course.')
        response = self.client.delete(f'/course/delete/{course.alias}/')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Course.DoesNotExist):
            course.refresh_from_db()
