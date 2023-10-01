from django.db import models


class Instructor(models.Model):
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    course_id = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    instructor_type = models.CharField(max_length=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "course_id"], name="unique_instructor"
            ),
            models.CheckConstraint(
                check=models.Q(instructor_type__in=["E", "T", "A"]),
                name="valid_type_of_instructor",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.user_id.get_full_name()} is "
            f"{self.instructor_type} in {self.course_id.alias}"
        )
