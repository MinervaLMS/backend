from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

# TODO: Entender exactamente para que sirve el atributo fields de estas Meta Class
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)