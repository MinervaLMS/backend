"""Module for the IO Code Submission model."""
from django.db import models
from courses.models.material import Material
from accounts.models.user import User


class IoCodeSubmission(models.Model):
    """Class that defines the model for the IO Code Submission table,
    which are the student's submmisions on each exercise."""

    submission_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )

    material_id = models.ForeignKey(Material, on_delete=models.CASCADE, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    submission_date = models.DateTimeField(auto_now=True, blank=False)
    code = models.CharField(blank=False)
    response_char = models.CharField(blank=True, null=True)
    execution_time = models.FloatField(blank=True, null=True)
    execution_memory = models.IntegerField(blank=True, null=True)
    completion_rate = models.FloatField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=False)

    class Meta:
        """Class that adds a constraint to the model."""

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    response_char__in={"A", "W", "I", "R", "O", "M", "T", "E", "C"}
                )
                | models.Q(response_char__isnull=True),
                name="char_check",
            )
        ]

    def __str__(self) -> str:
        """Method that returns a string representation of the model."""
        return f"{self.submission_id}"
