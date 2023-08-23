from django.db import models

from .course import Course

class Enrollment(models.Model):
    user_id = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, blank=False)
    course_id = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=False)
    enrollment_date = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # (user_id, course_id) pair is the primary key or the enrollment
                fields=['user_id', 'course_id'], name='unique_enrollment'),
        ]

    def __str__(self):
        return f'{self.user_id} enrollment in course {self.course_id}'
