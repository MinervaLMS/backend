from django.db import models

# from ...courses.models.material import Material
from courses.models.material import Material


class MaterialIoCode(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    material_id = models.OneToOneField(Material, on_delete=models.CASCADE, blank=False)
    max_time = models.IntegerField(blank=False)
    max_memory = models.IntegerField(blank=False)
    max_points = models.IntegerField(blank=False, null=False, default=0)
    min_points = models.IntegerField(blank=False, null=False, default=0)
    points_penalty = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f"{self.id}"
