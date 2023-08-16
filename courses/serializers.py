from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Material

class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = ['module_id', 'name', 'material_type', 'is_extra', 'order']

    def validate(self, data):
        """
        Verificar si la clave primaria module_id y order está duplicada.
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