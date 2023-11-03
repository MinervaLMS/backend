"""Module for views of IoCodeSubmission model."""
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..helpers.submission_summary import update_submission_summary
from ..serializers.io_code_submission_serializer import (
    IoCodeSubmissionSerializer,
    IoCodeSubmissionUserSerializer,
)
from ..models.io_code_submission import IoCodeSubmission
from ..schemas import io_code_submission_schemas as schemas


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_io_code_submission(request) -> JsonResponse:
    """
    View to create a code submission

    Args:
        request: http request with code submission data for creation

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    serializer = IoCodeSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        submission: IoCodeSubmission = serializer.save()
        # update submission summary for this user
        update_submission_summary(
            user=submission.user_id,
            material=submission.material_id,
            submission=submission,
        )
        return JsonResponse(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_io_code_submission(request, submission_id: int) -> JsonResponse:
    """
    Get code submission by its id

    Args:
        request: request http
        code_submission_id (int): code submission's id to get it

    Returns:
        Json response with the fields of the serialized code submission if the user
        making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    try:
        io_code_submission = IoCodeSubmission.objects.get(submission_id=submission_id)
        io_code_submission = IoCodeSubmissionSerializer(io_code_submission)
        return JsonResponse(
            io_code_submission.data, safe=False, status=status.HTTP_200_OK
        )
    except IoCodeSubmission.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a code submission with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_io_code_submission(request, submission_id: int) -> JsonResponse:
    """
    Delete code submission by its id

    Args:
        request: request http
        code_submission_id (int): code submission's id to get it

    Returns:
        Json response with the fields of the serialized code submission if the user
        making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    try:
        io_code_submission = IoCodeSubmission.objects.get(submission_id=submission_id)
        io_code_submission.delete()
        return JsonResponse(
            {"message": "Code submission was deleted successfully"},
            status=status.HTTP_200_OK,
        )
    except IoCodeSubmission.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a code submission with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_io_code_submission(request, submission_id: int) -> JsonResponse:
    """
    View to change material input-output video from a exercise in the database

    Args:
        request: request http with submission_id
        material_id (int): material's id to update it

        {
            "id": "id"
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    try:
        io_code_submission = IoCodeSubmission.objects.get(submission_id=submission_id)
    except IoCodeSubmission.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a Code Submission with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if "material_id" in request.data:
        io_code_submission.material_id = request.data["material_id"]
    if "user_id" in request.data:
        io_code_submission.user_id = request.data["user_id"]
    if "response_char" in request.data:
        io_code_submission.response_char = request.data["response_char"]
    if "execution_time" in request.data:
        io_code_submission.execution_time = request.data["execution_time"]
    if "execution_memory" in request.data:
        io_code_submission.execution_memory = request.data["execution_memory"]
    if "completion_rate" in request.data:
        io_code_submission.completion_rate = request.data["completion_rate"]

    io_code_submission.save()
    return JsonResponse(
        IoCodeSubmissionSerializer(io_code_submission).data,
        safe=False,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_io_code_all_submission_user_schema)
def get_io_code_all_submission_user(
    request, user_id: int, material_id: int
) -> JsonResponse:
    """
    Get all code submissions submitted by a user for a specific io_code

    Args:
        request: http request
        user_id: User's id to get his/her submissions
        material_id: Material's id to get its submissions

    Returns:
        Json response with the fields of the serialized code submission if the user
        making
        the request is Authenticated, else throws 401 Unauthorized status
    """
    submissions = IoCodeSubmission.objects.filter(
        user_id_id=user_id, material_id_id=material_id
    )

    if not submissions:
        return JsonResponse(
            {"message": "There are not submissions by that user for that io_code"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = IoCodeSubmissionUserSerializer(submissions, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
