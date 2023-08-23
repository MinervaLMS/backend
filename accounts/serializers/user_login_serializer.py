from rest_framework.serializers import Serializer
from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import User

class UserLoginSerializer(Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_auth = authenticate(**data)
        user_active = User.objects.filter(email=data['email'], is_active=True).exists()

        if not user_active:
            raise serializers.ValidationError("Please verify your email to login")

        if not user_auth:
            raise serializers.ValidationError("Incorrect Credentials")

        return user_auth