from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .course import Course


class Enrollment(models.Model):
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False)
    enrollment_date = models.DateTimeField(auto_now_add=True, blank=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    course_instructional_progress = models.IntegerField(default=0, blank=False)
    course_assessment_progress = models.IntegerField(default=0, blank=False)
    last_module = models.IntegerField(default=0, blank=False)

    appraisal_stars = models.IntegerField(
        blank=True, validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    appraisal_date = models.DateTimeField(null=True, blank=True)
    appraisal_comment = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # (user_id, course_id) pair is the primary key or the enrollment
                fields=["user_id", "course_id"],
                name="unique_enrollment",
            ),
        ]

    def __str__(self):
        return f"{self.user_id} enrollment in course {self.course_id}"
