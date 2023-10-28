"""Module for case serializer"""
from rest_framework import serializers

from ..models.case import Case


class CaseSerializer(serializers.ModelSerializer):
    """Class that defines the serializer for the Case model"""

    class Meta:
        model = Case
        fields = "__all__"

    def create(self, validated_data):
        """Method that creates a case"""
        case = Case(**validated_data)
        case.save()
        return case
