from rest_framework.serializers import ModelSerializer
from .models import User

# TODO: Añadir la función de create (Según entiendo es para que se serializen las contraseñas
#  automaticamente al crear un usuario)
class MinervaUserSerializer(ModelSerializer):
    """
    Minerva User serializer (for responses)
    """
    class Meta:
        model = User
        fields = '__all__'