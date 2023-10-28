"""Module for the Case model"""

from django.db import models
from .material_io_code import MaterialIoCode


class Case(models.Model):
    """Class that defines the model for the Case table
    which are the test cases for each exercise."""

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    id_case = models.IntegerField(null=True)
    input = models.TextField()
    output = models.TextField()
    material_io_code_id = models.ForeignKey(
        MaterialIoCode, on_delete=models.CASCADE, blank=False
    )
