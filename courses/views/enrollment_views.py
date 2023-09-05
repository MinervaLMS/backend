from django.http import JsonResponse
from django.db import models
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

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

    # Check if course exists
    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse(
            {"message": "Course not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Detect if user is enrolled in course
    user = request.user

    if not user.is_enrolled(alias):
        return JsonResponse(
            {"message": "You are not enrolled in this course"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Detect if user has already finished course
    enrollment = Enrollment.objects.annotate(
        total_stars=models.Sum("appraisal_stars")
    ).get(user_id=user, course_id=course)

    if not enrollment.completion_date:
        return JsonResponse(
            {"message": "You have not finished this course"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Detect if user has already appraised course
    # If so, update appraisal, date and comment
    if enrollment.appraisal_date:
        old_appraisal_stars = enrollment.appraisal_stars
        enrollment.appraisal_stars = request.data["stars"]
        enrollment.appraisal_comment = request.data["comment"]
        enrollment.appraisal_date = timezone.now()
        enrollment.save()

        # Update course average stars
        appraisal_difference = enrollment.appraisal_stars - old_appraisal_stars
        course.average_stars = (
            enrollment.total_stars + appraisal_difference
        ) / course.appraisals
        course.save()

        return JsonResponse(
            {"message": "Course appraised updated successfully"},
            status=status.HTTP_200_OK,
        )

    # Update Enrollment with appraisal, date and comment
    enrollment.appraisal_stars = request.data["stars"]
    enrollment.appraisal_comment = request.data["comment"]
    enrollment.appraisal_date = timezone.now()
    enrollment.save()

    # Update course average stars and number of appraisals
    course.appraisals += 1

    if not enrollment.total_stars:
        enrollment.total_stars = 0

    course.average_stars = (
        enrollment.total_stars + enrollment.appraisal_stars
    ) / course.appraisals
    course.save()

    return JsonResponse(
        {"message": "Course appraised successfully"}, status=status.HTTP_200_OK
    )
