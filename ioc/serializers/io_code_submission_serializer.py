"""Module for serializing IoCodeSubmission model"""

import requests
from rest_framework import serializers

from constants.ioc import URL_JUDGE
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
        serializer = IoCodeSubmissionSerializer(codesubmission)

        data = {
            "problem_id": serializer.data["material_id"],
            "submission_id": codesubmission.submission_id,
            "time_limit": codesubmission.execution_time,
            "memory_limit": codesubmission.execution_memory,
            "language": codesubmission.language,
            "code": codesubmission.code,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL_JUDGE, data=data, headers=headers)

        if response.status_code == 201:
            response_json = response.json()
            verdict = response_json.get("verdict")
            if verdict:
                verdict = verdict[0]
            codesubmission.response_char = verdict

        codesubmission.save()
        return codesubmission
