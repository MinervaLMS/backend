"""Module for serializing IoCodeSubmission model"""

import json
import requests
from rest_framework import serializers

from constants.ioc import URL_JUDGE

from ..models.io_code_submission import IoCodeSubmission
from ..models.material_io_code import MaterialIoCode


def judge(codesubmission, material_ioc):
    """Method that sends a request to the judge to evaluate the code submission"""

    data = {
        "code": codesubmission.code,
        "submission_id": codesubmission.submission_id,
        "problem_id": str(codesubmission.material_id.id),
        "time_limit": material_ioc.max_time,
        "memory_limit": material_ioc.max_memory,
        "language": codesubmission.language,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(URL_JUDGE, data=json.dumps(data), headers=headers)

    return response.json(), response.status_code


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
        material_ioc = MaterialIoCode.objects.filter(
            material_id=codesubmission.material_id.id
        ).first()

        response, status_code = judge(codesubmission, material_ioc)

        if status_code == 201:
            if (
                response["verdict"]
                == "Judge execution: code compilation or problem_id don't exist."
            ):
                codesubmission.response_char = "C"
                codesubmission.execution_memory = 0
                codesubmission.execution_time = 0
                codesubmission.save()
            else:
                codesubmission.response_char = response["verdict"]["verdict"][0]
                codesubmission.execution_memory = response["max_memory"]
                codesubmission.execution_time = response["max_time"]
                codesubmission.save()

        return codesubmission

    def to_representation(self, instance):
        """Method that returns a representation of the model"""
        return {
            "verdict": instance.response_char,
            "execution_time": instance.execution_time,
            "execution_memory": instance.execution_memory,
        }
