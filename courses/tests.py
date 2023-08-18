from django.test import TestCase
from rest_framework.test import APIClient

from .models import Course, Material
from accounts.models import User

#TODO: repeat test to create material when the order attribute is fixed (AutoIncrement)

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

# class CreateMaterialTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create(email='test@example.com', password='testpassword')
#         self.client.force_authenticate(self.user)

#         self.material_data = {
#             "module_id": 4,
#             "name": "Image to reply", 
#             "material_type": "png",
#             "is_extra": True,
#             "order": 1 
#         }

#         self.material_invalid_types = {
#             "module_id": 4,
#             "name": "Papiro", 
#             "material_type": True,
#             "is_extra": 2,
#             "order": "first" 
#         }

#     def test_create_correct(self):
#         response = self.client.post('/material/create/', self.material_data, format='json')
#         self.assertEqual(response.status_code, 201)

#     def test_create_blank(self):
#         response = self.client.post('/material/create/', {}, format='json')
#         self.assertEqual(response.status_code, 400)

#     def test_create_invalid_types(self):
#         response = self.client.post('/material/create/', self.material_invalid_types, format='json')
#         self.assertEqual(response.status_code, 400)

class GetMaterialByModuleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient
        self.user = User.objects.create(email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)

    # A module should be created to carry out this test 

class GetMaterialTestCase(TestCase):
    def setUp(self):
        self.client = APIClient
        self.user = User.objects.create(email='test@example.com', password='testpassword')
        self.client.force_authenticate(self.user)

        # I should know the material's id

class UpdateMaterialTestCase(TestCase):
    # I should know the material's id
    pass


class UpdateMaterialOrderTestCase(TestCase):
    # I should know the module's id from which I want to order materials
    pass

class DeleteMaterialTestCase(TestCase):
    # I should know the material's id that I want to delete
    pass