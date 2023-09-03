from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..models.user import User


class UserSerializer(ModelSerializer):
    # write_only means that the field will not be returned in the response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
