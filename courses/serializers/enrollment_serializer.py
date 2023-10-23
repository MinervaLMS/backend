from rest_framework import serializers
from ..models.enrollment import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"

    def create(self, validated_data):
        enrollment: Enrollment = Enrollment(**validated_data)
        enrollment.save()
        return enrollment
