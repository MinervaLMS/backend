from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

# TODO: cambiar username a email para registro con email unico
# TODO: cuando se cambie el uso de unique de username a email, cambiar todos los "username" a "email"
# TODO: Entender exactamente para que sirve el atributo fields de estas Meta Class
class MinervaUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class MinervaUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)