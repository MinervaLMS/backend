from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from ..schemas import enrollment_schemas as schemas
from ..models.enrollment import Enrollment
from ..models.course import Course


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@schema(schemas.appraise_course_schema)
def appraise_course(request, alias) -> JsonResponse:
    """
    View to appraise a course. Only enrolled users can appraise a course.

    Args:
        request: Json request with the following fields: stars, comment
        alias (string): Course alias

    Returns:
        JsonResponse: Json response with a message and a status code
    """

    # Check required fields
    required_fields: list = ["stars", "comment"]
    error_messages: dict = {}

    for field in required_fields:
        if field not in request.data:
            error_messages[field] = "This field is required"

    if "stars" in request.data and request.data["stars"] not in range(0, 11):
        error_messages["stars"] = "Stars must be between 0 and 10"

    if error_messages:
        return JsonResponse(error_messages, status=status.HTTP_400_BAD_REQUEST)

    # Detect if user is enrolled in course
    user = request.user

    if not user.is_enrolled(alias):
        return JsonResponse(
            {"message": "You are not enrolled in this course"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Detect if user has already finished course
    course = Course.objects.get(alias=alias)
    enrollment = Enrollment.objects.get(user_id=user, course_id=course)

    if not enrollment.completion_date:
        return JsonResponse(
            {"message": "You have not finished this course"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Detect if user has already appraised course
    # If so, update appraisal, date and comment
    if enrollment.appraisal_date:
        enrollment.appraisal_stars = request.data["stars"]
        enrollment.appraisal_comment = request.data["comment"]
        enrollment.appraisal_date = datetime.now()
        enrollment.save()

        return JsonResponse(
            {"message": "Course appraised updated successfully"},
            status=status.HTTP_200_OK,
        )

    # Update Enrollment with appraisal, date and comment
    enrollment.appraisal_stars = request.data["stars"]
    enrollment.appraisal_comment = request.data["comment"]
    enrollment.appraisal_date = datetime.now()
    enrollment.save()

    return JsonResponse(
        {"message": "Course appraised successfully"}, status=status.HTTP_200_OK
    )
