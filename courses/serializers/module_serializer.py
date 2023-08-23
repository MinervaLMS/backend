from rest_framework import serializers

from ..models import Course, Module

class ModuleSerializer(serializers.ModelSerializer):
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