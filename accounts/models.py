from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from courses.models import Course, Enrollment

# TODO: Add many to many relationship with courses using instructor

class User(AbstractUser):
    """
    Edited user model to use email as username, timestamp as id and change required fields
    """

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID', editable=False)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=False)

    # Many to many relationships
    courses = models.ManyToManyField('courses.Course', through='courses.Enrollment')

    # Remove username field and use email as unique identifier
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Use custom user manager
    objects = UserManager()

    # Temporary enroll all registered users to ED20241 course
    def save(self, *args, **kwargs):
        course = apps.get_model('courses', 'Course').objects.get(alias="ED20241")
        already_enrolled = Enrollment.objects.filter(user_id=self, course_id=course).exists()

        if not already_enrolled:
            enrollment = Enrollment(user_id=self, course_id=course)
            enrollment.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return(self.get_full_name())