from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    """
    Edited user model to use email as username, timestamp as id and change required fields
    """

    id = models.BigIntegerField(primary_key=True, editable=False)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    # Remove username field and use email as unique identifier
    username=None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Use custom user manager
    objects = UserManager()

    def save(self, *args, **kwargs):
        """
        Use timestamp in milliseconds as id when user is created
        """
        if not self.id:
            self.id = int(datetime.now().timestamp() * 1000)

        super().save(*args, **kwargs)

    def __str__(self):
        return(self.get_full_name())