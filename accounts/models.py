from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MinervaUserManager
from datetime import datetime

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
    id=models.BigIntegerField(primary_key=True, editable=False)
    # class Meta:
    #     db_table = 'user'
    #     # Indica el valor inicial y el incremento para el campo AutoField
    #     # El valor de 'start_with' establece el valor inicial, y 'increment_by' establece el incremento
    #     options = {'starting_value': 1000, 'increment_by': 1}

    objects = MinervaUserManager()
    def __str__(self):
        return(self.get_full_name())
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = int(datetime.now().timestamp() * 1000)
        super().save(*args, **kwargs)