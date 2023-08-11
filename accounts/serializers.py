from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import User

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True) # write_only means that the field will not be returned in the response
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

class UserLoginSerializer(Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError("Incorrect Credentials")