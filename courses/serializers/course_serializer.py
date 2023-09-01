from rest_framework import serializers

from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "alias", "description"]
