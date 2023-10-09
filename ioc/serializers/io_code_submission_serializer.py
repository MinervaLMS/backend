"""Module for serializing IoCodeSubmission model"""

import json
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
        codesubmission.save()

        data = {
            "problem_id": serializer.data["material_id"],
            "submission_id": codesubmission.submission_id,
            "code": codesubmission.code,
            "time_limit": codesubmission.execution_time,
            "memory_limit": codesubmission.execution_memory,
            "language": codesubmission.language,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL_JUDGE, data=json.dumps(data), headers=headers)
        print(data, response)

        if response.status_code == 201:
            response_json = response.json()
            verdict_dict = response_json.get("verdict")
            print(verdict_dict)
            if verdict_dict:
                verdict = verdict_dict.get("verdict")
                codesubmission.response_char = verdict[0]
                codesubmission.save()
        return codesubmission
