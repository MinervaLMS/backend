from django.db import models

from .material import Material


class MaterialHTML(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    material_id = models.OneToOneField(Material, on_delete=models.CASCADE, blank=False)

    # Max Markdown storage is about 100kB
    content = models.TextField(blank=False, max_length=100000)

    def __str__(self):
        return f"{self.material_id} content"
