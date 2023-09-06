from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from courses.models.course import Course
from courses.models.enrollment import Enrollment
from institutions.models.institution import Institution

# TODO: Add many to many relationship with courses using instructor
# TODO: Delete the temporary enrollment to ED20241 course in production


class User(AbstractUser):
    """
    Custom user model to use email as username and changed required fields
    """

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    email = models.EmailField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=False)

    # Many to many relationships
    courses = models.ManyToManyField("courses.Course", through="courses.Enrollment")
    materials = models.ManyToManyField("courses.Material", through="courses.Access")

    # Remove username field and use email as unique identifier
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Use custom user manager
    objects = UserManager()

    # Temporary enroll all registered users to ED20241 course
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            course = Course.objects.get(alias="ED")
        except Course.DoesNotExist:
            institution = Institution.objects.create(
                name="Universidad Nacional de Colombia",
                alias="UNAL",
                description="UNAL description",
                url="https://unal.edu.co/",
            )
            course = Course.objects.create(
                name="Estructuras de Datos",
                alias="ED",
                institution=institution,
            )
            course.save()

        already_enrolled = Enrollment.objects.filter(
            user_id=self, course_id=course
        ).exists()

        if not already_enrolled:
            enrollment = Enrollment(user_id=self, course_id=course)
            enrollment.save()

    # Method to check if user is enrolled in a course with given alias
    def is_enrolled(self, alias):
        try:
            course = Course.objects.get(alias=alias)
        except Course.DoesNotExist:
            return False

        return Enrollment.objects.filter(user_id=self, course_id=course).exists()

    def __str__(self):
        return self.get_full_name()
