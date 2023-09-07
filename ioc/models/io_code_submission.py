from django.db import models
from courses.models.material import Material
from accounts.models.user import User


class IoCodeSubmission(models.Model):
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
    response_char = models.CharField(max_length=1, blank=False)
    execution_time = models.IntegerField(blank=False)
    execution_memory = models.IntegerField(blank=False)
    completion_rate = models.FloatField(blank=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(response_char__in={"A", "W", "C", "E", "T"}),
                name="char_check",
            )
        ]

    def __str__(self):
        return f"{self.submission_id}"
