from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers

class MinervaUserSerializer(ModelSerializer):
    """
    Minerva User serializer (for responses)
    """
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user