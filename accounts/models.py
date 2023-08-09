from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MinervaUserManager

# Create your models here.
# TODO: cambiar el uso de unique username a unique email
class User(AbstractUser):
    """
    Using to extend the User model
    """
    #picture = models.ImageField(null=True, blank=True, upload_to='users/', default='users/defaultUser.png')
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    

    objects = MinervaUserManager()
    def __str__(self):
        return(self.get_full_name())