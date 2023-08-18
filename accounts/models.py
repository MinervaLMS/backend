from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    """
    Edited user model to use email as username, timestamp as id and change required fields
    """

    id = models.BigAutoField(primary_key=True, editable=False)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=False)

    # Remove username field and use email as unique identifier
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Use custom user manager
    objects = UserManager()

    def __str__(self):
        return (self.get_full_name())
