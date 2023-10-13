from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from json import loads

from ..models.comment import Comment

from courses.models.course import Course
from courses.models.module import Module
from courses.models.material import Material
from accounts.models.user import User
from institutions.models.institution import Institution


class CreateCommentTestCase(TestCase):
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
        self.comment_data = {
            "material_id": self.material.id,
            "user_id": self.user.id,
            "content": "Test comment",
        }
        self.client.force_authenticate(self.user)

    def test_create_comment_user_not_exist(self):
        data = {
            "material_id": self.material.id,
            "user_id": -self.user.id,
            "content": "Test comment",
        }
        response = self.client.post("/comment/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a user with this id"}
        )

    def test_create_comment_material_not_exist(self):
        data = {
            "material_id": -self.material.id,
            "user_id": self.user.id,
            "content": "Test comment",
        }
        response = self.client.post("/comment/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content), {"message": "There is not a material with this id"}
        )

    def test_create_comment_not_enrolled(self):
        course_temp = Course.objects.create(
            name="Web Development",
            alias="WD",
            institution=self.institution,
        )
        module_temp = Module.objects.create(
            course_id=course_temp,
            name="Test module",
        )
        material_temp = Material.objects.create(
            module_id=module_temp,
            name="Test material",
            material_type="pdf",
        )
        comment_data = {
            "material_id": material_temp.id,
            "user_id": self.user.id,
            "content": "Test comment",
        }

        response = self.client.post("/comment/create/", comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            loads(response.content),
            {"message": "You do not have permission to comment this material"},
        )

    def test_createe_comment_correct(self):
        response = self.client.post(
            "/comment/create/", self.comment_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)


class GetCommentTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_get_comment_nonexistent(self):
        response = self.client.get("/comment/11000/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a comment with this id"},
        )

    def test_get_comment_correct(self):
        response = self.client.get(f"/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.last().content, "Test comment")


class GetCommentRepliesTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.comment2 = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment2"
        )

        self.reply = Comment.objects.create(
            material_id=self.material,
            user_id=self.user,
            parent_comment_id=self.comment,
            content="Test comment reply",
        )

        self.client.force_authenticate(self.user)

    def test_get_comment_replies_nonexistent(self):
        response = self.client.get("/comment/11000/replies/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a comment with this id"},
        )

    def test_get_comment_replies_correct(self):
        response = self.client.get(f"/comment/{self.comment.id}/replies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(loads(response.content)), 1)

    def test_get_comment_replies_empty(self):
        response = self.client.get(f"/comment/{self.comment2.id}/replies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content), {"message": "This comment has not replies"}
        )


class UpdateCommentFixedTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_update_comment_fixed_nonexistent(self):
        response = self.client.patch("/comment/update/11000/", {"fixed": 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a comment with this id"},
        )

    def test_update_comment_fixed_correct(self):
        response = self.client.patch(
            f"/comment/update/{self.comment.id}/", {"fixed": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.last().fixed, 1)
        self.assertEqual(
            loads(response.content),
            {"message": "Comment updated successfully"},
        )


class DeleteCommentTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_delete_comment_nonexistent(self):
        response = self.client.delete(f"/comment/delete/{self.comment.id+1}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a comment with this id"},
        )

    def test_delete_comment_correct(self):
        response = self.client.delete(f"/comment/delete/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(
            loads(response.content), {"message": "Comment deleted successfully"}
        )


class GetMaterialCommentsTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_get_material_comments_nonexistent(self):
        response = self.client.get(f"/material/{self.material.id+1}/comments/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not a material with this id"},
        )

    def test_get_material_comments_correct(self):
        response = self.client.get(f"/material/{self.material.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(loads(response.content)), 1)


class GetUserCommentsTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_get_user_comments_nonexistent(self):
        response = self.client.get(
            f"/users/{self.user.id+1}/comments/{self.material.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response.content),
            {"message": "There is not an user with this id"},
        )

    def test_get_user_comments_empty(self):
        user_temp = User.objects.create(
            email="test2@example.com",
            password="testpassword2",
            last_name="test_last_name2",
            first_name="test_first_name2",
        )
        response = self.client.get(
            f"/users/{user_temp.id}/comments/{self.material.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            {"message": "This user does not have comments in this material"},
        )

    def test_get_user_comments_correct(self):
        response = self.client.get(
            f"/users/{self.user.id}/comments/{self.material.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(loads(response.content)), 1)


class UpdateUserCommentsTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_update_user_comment_nonexistent(self):
        response1 = self.client.patch(
            f"/users/update/{self.user.id+1}/comment/{self.comment.id}/",
            {"content": "Test comment updated"},
            format="json",
        )
        response2 = self.client.patch(
            f"/users/update/{self.user.id}/comment/{self.comment.id+1}/",
            {"content": "Test comment updated"},
            format="json",
        )
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response1.content),
            {"message": "There is not an user with this id"},
        )
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response2.content),
            {"message": "There is not a comment with this id for this user"},
        )

    def test_update_user_comment_nocontent(self):
        response = self.client.patch(
            f"/users/update/{self.user.id}/comment/{self.comment.id}/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            loads(response.content),
            {"message": "Content is required"},
        )

    def test_update_user_comment_correct(self):
        response = self.client.patch(
            f"/users/update/{self.user.id}/comment/{self.comment.id}/",
            {"content": "Test comment updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            loads(response.content),
            {"message": "Comment updated successfully"},
        )
        self.assertEqual(Comment.objects.last().content, "Test comment updated")


class DeleteUserCommentsTestCase(TestCase):
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
        self.comment = Comment.objects.create(
            material_id=self.material, user_id=self.user, content="Test comment"
        )

        self.client.force_authenticate(self.user)

    def test_delete_user_comment_nonexistent(self):
        response1 = self.client.delete(
            f"/users/delete/{self.user.id+1}/comment/{self.comment.id}/"
        )
        response2 = self.client.delete(
            f"/users/delete/{self.user.id}/comment/{self.comment.id+1}/"
        )
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response1.content),
            {"message": "There is not an user with this id"},
        )
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            loads(response2.content),
            {"message": "There is not a comment with this id for this user"},
        )

    def test_delete_user_comment_correct(self):
        response = self.client.delete(
            f"/users/delete/{self.user.id}/comment/{self.comment.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(
            loads(response.content), {"message": "Comment deleted successfully"}
        )
