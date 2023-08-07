from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MinervaUserManager

# Create your models here.
# TODO: cambiar el uso de unique username a unique email
class User(AbstractUser):
    """
    Using to extend the User model
    """
    picture = models.ImageField(null=True, blank=True, upload_to='users/', default='users/defaultUser.png')

    

    objects = MinervaUserManager()