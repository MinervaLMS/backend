from django.db import models


class Course(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    name = models.CharField(max_length=100, blank=False, unique=True)
    alias = models.CharField(max_length=20, blank=False, unique=True)
    description = models.TextField(blank=True)

    enrollments = models.ManyToManyField("accounts.User", through="Enrollment")

    def __str__(self):
        return self.alias
