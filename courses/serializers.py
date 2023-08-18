from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from rest_framework import serializers
from .models import Course

from .models import Material

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'alias', 'description']
        

class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"

    def validate(self, data):
        """
        Verify if unique tuple module_id and order is duplicated.
        """
        module_id = data.get('module_id')
        order = data.get('order')

        if Material.objects.filter(module_id=module_id, order=order).exists():
            raise serializers.ValidationError("This order in this module is already in use")
        
        return data
    def create(self, validated_data):
        material = Material(**validated_data)
        material.save()
        return material