from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    alias = models.CharField(max_length=20, blank=False, unique=True)
    description = models.CharField(max_length=1024)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name
