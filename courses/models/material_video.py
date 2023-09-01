from django.db import models

from .material import Material

class MaterialVideo(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True,
                             serialize=False, verbose_name='ID', editable=False)
    material_id = models.OneToOneField(Material, on_delete=models.CASCADE, blank=False)
    length = models.IntegerField(blank=False)
    source = models.CharField(max_length=1, blank=False)
    external_id = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.external_id}'