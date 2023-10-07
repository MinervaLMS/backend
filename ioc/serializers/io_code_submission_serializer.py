"""Module for serializing IoCodeSubmission model"""

import json
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

        data = {
            "code": "print(int(input())**2)",
            "submission": "EDM05E0",
            "input": ["4\n1 2 3 4", "8\n1 5 2 3 2 3 4 5"],
            "output": ["La suma es 10", "La suma es 25"],
            "time_limit": 5000,
            "memory_limit": 256,
            "language": "py3"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL_JUDGE, data=json.dumps(data), headers=headers) 
        
        if response.status_code == 201:
            response_json = response.json()
            verdict = response_json.get("verdict")
            if verdict=="AC":
                verdict="A"
            else:
                verdict="W"
            codesubmission.set_response_char(verdict)

        codesubmission.save()
        return codesubmission
