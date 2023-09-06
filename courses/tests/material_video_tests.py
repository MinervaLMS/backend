from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.course import Course
from ..models.module import Module
from ..models.material import Material
from ..models.material_video import MaterialVideo

from accounts.models.user import User


class CreateMaterialVideoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="VID",
            is_extra=True,
        )

        self.material_video_data = {
            "material_id": self.material.id,
            "external_id": "https://www.youtube.com/watch?v=gvYrBbX6obo&amp;ab_channel=DeiGamer",
        }

        self.material_video_invalid_types = {
            "material_id": self.material.id,
            "external_id": "https://www.google.com"
        }

        self.client.force_authenticate(self.user)

    def test_create_correct(self):
        response = self.client.post(
            "/material/video/create/", self.material_video_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_blank(self):
        response = self.client.post("/material/video/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_types(self):
        response = self.client.post(
            "/material/video/create/", self.material_video_invalid_types, format="json"
        )
        self.assertEqual(response.status_code, 400)


class GetMaterialVideoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")

        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material",
            material_type="VID",
            is_extra=True,
        )

        self.material_video_data = {
            "material_id": self.material.id,
            "external_id": "https://www.youtube.com/watch?v=gvYrBbX6obo&amp;ab_channel=DeiGamer",
        }

        self.materialVideo = MaterialVideo.objects.create(
            material_id=self.material,
            external_id="https://www.youtube.com/watch?v=gvYrBbX6obo&amp;ab_channel=DeiGamer",
            length=954
        )

        self.client.force_authenticate(self.user)

    def test_get_material_video_correct(self):
        response = self.client.get(f"/material/video/{self.material.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_material_video_not_exist(self):
        response = self.client.get("/material/video/234/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateMaterialVideoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material name",
            material_type="vid",
            is_extra=True,
        )

        self.materialVideo = MaterialVideo.objects.create(
            material_id=self.material,
            external_id="https://www.youtube.com/watch?v=gvYrBbX6obo&amp;ab_channel=DeiGamer",
            length=954
        )

        self.material_video_update_data = {
            "external_id": "https://www.youtube.com/watch?v=Rm-jFWy7Jx0&ab_channel=JekavacTV"
        }

        self.material_video_source_fail_fields = {"external_id": "https://www.youtube.com/watch?v=Rm-jFWy7Jx0&ab_channel=JekavacTV", "source": "H"}

        self.material_video_length_fail_fields = {"external_id": "https://www.youtube.com/watch?v=Rm-jFWy7Jx0&ab_channel=JekavacTV", "length": 234}

        self.material_video_source_fail_fields = {"external_id": "https://www.google.com"}

        self.material_video_fail_fields = {"external_id": "https://www.youtube.com/watch?v=Rm-jFWy7Jx0&ab_channel=JekavacTV", "name": "imposible"}

        self.client.force_authenticate(self.user)

    def test_update_material_video_not_exist(self):
        response = self.client.patch(
            "/material/video/update/2344/", self.material_video_update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with that id"}
        )

    def test_update_material_video_source(self):
        response = self.client.patch(
            f"/material/video/update/{self.material.id}/",
            self.material_video_source_fail_fields,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "You can not change the source of a video manually"},
        )

    def test_update_material_video_length(self):
        response = self.client.patch(
            f"/material/video/update/{self.material.id}/",
            self.material_video_length_fail_fields,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "You can not change the length of a video manually"},
        )

    def test_update_material_video_source(self):
        response = self.client.patch(
            f"/material/video/update/{self.material.id}/",
            self.material_video_source_fail_fields,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "The external_id should be a valid YouTube link"},
        )

    def test_update_material_video_fail_fields(self):
        response = self.client.patch(
            f"/material/video/update/{self.material.id}/",
            self.material_video_fail_fields,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "name attribute does not exist in material"},
        )

    def test_update_material_video_correct(self):
        response = self.client.patch(
            f"/material/video/update/{self.material.id}/",
            self.material_video_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMaterialVideoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            name="Test Course", alias="ED20241", description="This is a test course"
        )
        self.user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            last_name="test_last_name",
            first_name="test_first_name",
        )
        self.module = Module.objects.create(course_id=self.course, name="Test module")
        self.material = Material.objects.create(
            module_id=self.module,
            name="Test material_1",
            material_type="png",
            is_extra=True,
        )

        self.materialVideo = MaterialVideo.objects.create(
            material_id=self.material,
            external_id="https://www.youtube.com/watch?v=gvYrBbX6obo&amp;ab_channel=DeiGamer",
            length=954
        )

        self.client.force_authenticate(self.user)

    def test_material_video_delete_not_exist(self):
        response = self.client.delete(f"/material/video/delete/{self.materialVideo.id + 1}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_delete_correct(self):
        response = self.client.delete(f"/material/video/delete/{self.materialVideo.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
