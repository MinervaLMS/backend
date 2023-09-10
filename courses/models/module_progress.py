from django.db import models
from .module import Module
from accounts.models.user import User


class Module_progress(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, primary_key=True)
    module_id = models.ForeignKey(
        Module, on_delete=models.CASCADE, primary_key=True)
    module_instructional_progress = models.IntegerField(default=0)
    module_assessment_progress = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # One module per user
                fields=["user_id", "module_id"],
                name="unique_user_module",
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.module_id}"
