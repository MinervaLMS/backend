from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from rest_framework import serializers
from .models import Course, Module, Material


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
            raise serializers.ValidationError(
                "This order in this module is already in use")

        return data

    def create(self, validated_data):
        material = Material(**validated_data)
        material.save()
        return material


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

    def validate(self, data):
        """
        Verify if unique tuple course_id and order is duplicated, Verify course_id and name, verify if course exists.
        """
        alias = data.get('course_id')
        name = data.get('name')
        order = data.get('order')
        if Module.objects.filter(course_id=alias, order=order).exists():
            raise serializers.ValidationError(
                "This order in this course is already in use")

        if Module.objects.filter(course_id=alias, name=name).exists():
            raise serializers.ValidationError(
                "This name in this course is already in use")

        if not Course.objects.filter(alias=alias).exists():
            raise serializers.ValidationError(
                "This course does not exist")
        return data

    def create(self, validated_data):
        module = Module(**validated_data)
        module.save()
        return module
