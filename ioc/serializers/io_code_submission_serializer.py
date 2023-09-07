from rest_framework import serializers

from ..models.io_code_submission import IoCodeSubmission


class IoCodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoCodeSubmission
        fields = "__all__"

    def create(self, validated_data):
        codesubmission = IoCodeSubmission(**validated_data)
        codesubmission.save()
        return codesubmission
