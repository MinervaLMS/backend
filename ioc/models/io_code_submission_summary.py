from django.db import models

from courses.models.material import Material
from accounts.models.user import User


class IoCodeSubmissionSummary(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="submission_summary"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submission_summary"
    )
    attempts = models.IntegerField(default=1)
    hits = models.IntegerField()
    points = models.IntegerField()
    min_execution_time = models.FloatField()
    min_execution_memory = models.IntegerField()
    max_completion_rate = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # (user, material) pair is the primary key or
                # the IoCodeSubmissionSummary
                fields=["user", "material"],
                name="unique_io_code_submission_summary",
            ),
        ]

    def __str__(self):
        return f"{self.user} has sent this code material: {self.material}"
