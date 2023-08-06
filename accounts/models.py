from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    picture = models.ImageField(null=True, blank=True, upload_to='users/', default='users/defaultUser.png')