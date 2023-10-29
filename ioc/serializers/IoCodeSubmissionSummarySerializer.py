from rest_framework import serializers

from ..models.io_code_submission_summary import IoCodeSubmissionSummary


class IoCodeSubmissionSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = IoCodeSubmissionSummary
        fields = "__all__"
        read_only_fields = (
            "submission_summary_id",
            "material",
            "user",
            "attempts",
            "hits",
            "points",
            "min_execution_time",
            "min_execution_memory",
            "max_completion_rate",
        )