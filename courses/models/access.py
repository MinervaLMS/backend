from django.db import models

from .material import Material


class Access(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    views = models.IntegerField(default=1)
    last_view = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(null=True, blank=True)
    like = models.BooleanField(null=True, blank=True)

    class Meta:
        constraints = [
            # (material_id, user_id) pair is the primary key or the access
            models.UniqueConstraint(
                fields=["material_id", "user_id"], name="unique_access"
            )
        ]

    def __str__(self) -> str:
        return f"user {self.user_id} accessed to material {self.material_id}"
