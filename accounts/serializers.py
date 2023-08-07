from rest_framework.serializers import ModelSerializer
from .models import User


class MinervaUserSerializer(ModelSerializer):
    """
    Minerva User serializer (for responses)
    """
    class Meta:
        model = User
        fields = '__all__'