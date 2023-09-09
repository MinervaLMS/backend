'''Module for serializing IoCodeSubmission model'''

from rest_framework import serializers
from ..models.io_code_submission import IoCodeSubmission


class IoCodeSubmissionSerializer(serializers.ModelSerializer):
    '''Class that serializes the IoCodeSubmission model'''

    class Meta:
        '''Class that defines the metadata for the serializer,
        in this case serialezes all the fields'''

        model = IoCodeSubmission
        fields = "__all__"

    def create(self, validated_data)->IoCodeSubmission:
        '''Method that creates a new IoCodeSubmission
         instance whit the validated data'''

        codesubmission = IoCodeSubmission(**validated_data)
        codesubmission.save()
        return codesubmission
