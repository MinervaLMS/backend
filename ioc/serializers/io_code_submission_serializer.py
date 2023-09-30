"""Module for serializing IoCodeSubmission model"""

import requests
from rest_framework import serializers

from constants.constants import URL_JUDGE
from ..models.io_code_submission import IoCodeSubmission


class IoCodeSubmissionSerializer(serializers.ModelSerializer):
    """Class that serializes the IoCodeSubmission model"""

    class Meta:
        """Class that defines the metadata for the serializer,
        in this case serialezes all the fields"""

        model = IoCodeSubmission
        fields = "__all__"

    def create(self, validated_data) -> IoCodeSubmission:
        """Method that creates a new IoCodeSubmission
        instance whit the validated data"""

        codesubmission = IoCodeSubmission(**validated_data)
        codesubmission.save()

        data = {"code_submission": codesubmission}
        requests.post(URL_JUDGE, data=data)

        return codesubmission
