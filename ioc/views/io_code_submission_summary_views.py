from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..schemas import io_code_submission_summary_schemas as schemas
from ioc.models import IoCodeSubmissionSummary
from ioc.serializers.IoCodeSubmissionSummarySerializer import IoCodeSubmissionSummarySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_summary_by_user_schema)
def get_summary_by_user(request, user_id:int, material_id:int) -> JsonResponse:
    """
    Get code submission summary by user and material

    Args:
        request: http request
        user_id: User's id to get his/her submission summary
        material_id: Material's id to get its submission summary
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    try:
        submission_summary = IoCodeSubmissionSummary.objects.get(user_id=user_id, material_id=material_id)
        submission_summary = IoCodeSubmissionSummarySerializer(submission_summary)
        return JsonResponse(
            submission_summary.data,
            status=status.HTTP_200_OK,
        )
    except IoCodeSubmissionSummary.DoesNotExist:
        return JsonResponse(
            {"message": "Submission summary does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )