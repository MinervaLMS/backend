from django.test import TestCase
from rest_framework.test import APIClient

from ..models.institution import Institution
from accounts.models.user import User


class CreateInstitutionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution_data = {
            "name": "Institucion de Test",
            "alias": "IT",
            "description": "Institucion de Test",
            "url": "https://www.instituciontest.com",
        }

    def test_create_institution_correct(self):
        response = self.client.post(
            "/institution/create/", self.institution_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_institution_invalid_data(self):
        invalid_data = {
            "name": "",  # Invalid name
            "alias": "IT",
            "description": "Institucion de Test",
            "url": "https://www.instituciontest.com",
        }
        response = self.client.post("/institution/create/", invalid_data, format="json")
        self.assertEqual(response.status_code, 400)


class GetInstitutionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
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

    def test_get_institution_correct(self):
        response = self.client.get("/institution/{}/".format(self.institution.id))
        self.assertEqual(response.status_code, 200)

    def test_get_institution_not_found(self):
        response = self.client.get("/institution/get/100/")
        self.assertEqual(response.status_code, 404)


class UpdateInstitutionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
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

    def test_update_institution_correct(self):
        institution_data = {
            "name": "Institucion de Test Actualizada",
            "alias": "ITA",
            "description": "Institucion de Test Actualizada",
            "url": "https://www.instituciontestactualizada.com",
        }
        response = self.client.patch(
            "/institution/update/{}/".format(self.institution.id),
            institution_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_institution_not_found(self):
        institution_data = {
            "name": "Institucion de Test Actualizada",
            "alias": "ITA",
            "description": "Institucion de Test Actualizada",
            "url": "https://www.instituciontestactualizada.com",
        }
        response = self.client.patch(
            "/institution/update/100/", institution_data, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_institution_invalid_data(self):
        institution_data = {
            "name": "",  # Invalid name
            "alias": "ITA",
            "description": "Institucion de Test Actualizada",
            "url": "https://www.instituciontestactualizada.com",
        }
        response = self.client.patch(
            "/institution/update/{}/".format(self.institution.id),
            institution_data,
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class DeleteInstitutionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)
        self.institution_data = {
            "name": "Institucion de Test",
            "alias": "IT",
            "description": "Institucion de Test",
            "url": "https://www.instituciontest.com",
        }

    def test_delete_institution_correct(self):
        institution = Institution.objects.create(**self.institution_data)
        response = self.client.delete("/institution/delete/{}/".format(institution.id))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Institution.DoesNotExist):
            institution.refresh_from_db()

    def test_delete_institution_not_found(self):
        response = self.client.delete("/institution/delete/100/")
        self.assertEqual(response.status_code, 404)
