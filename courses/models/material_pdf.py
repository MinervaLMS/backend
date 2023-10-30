from django.db import models

from .material import Material


class MaterialPDF(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    material_id = models.OneToOneField(Material, on_delete=models.CASCADE, blank=False)

    url = models.TextField(blank=False, max_length=1000)
    pages = models.PositiveIntegerField(blank=False, default=1)

    def __str__(self):
        return f"PDF of material {self.material_id}"
