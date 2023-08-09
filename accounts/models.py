from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MinervaUserManager
from datetime import datetime

class User(AbstractUser):
    """
    Using to extend the User model
    """
    #picture = models.ImageField(null=True, blank=True, upload_to='users/', default='users/defaultUser.png')
    id=models.BigIntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MinervaUserManager()

    def __str__(self):
        return(self.get_full_name())
    
    def save(self, *args, **kwargs):
        """
        This function create a new user with timestamp as Id
        """
        if not self.id:
            self.id = int(datetime.now().timestamp() * 1000)
        super().save(*args, **kwargs)