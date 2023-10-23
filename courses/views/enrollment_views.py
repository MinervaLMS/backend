from django.http import JsonResponse
from django.db import models
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models.user import User
from ..models.enrollment import Enrollment
from ..models.course import Course
from ..schemas import enrollment_schemas as schemas

from ..serializers.enrollment_serializer import EnrollmentSerializer
from ..helpers.create_all_accesses import create_accesses_for_user


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@schema(schemas.create_enrollment_schema)
def create_enrollment(request) -> JsonResponse:
    """
    Create an enrollment for a user in a course
    Args:
        request: http request with user's id and course's alias to create the enrollment
    Returns:
        JsonResponse: Json response with a message and a status code
    """
    try:
        user: User = User.objects.get(id=request.data["user_id"])
        course: Course = Course.objects.get(alias=request.data["course_alias"])

        request.data["course_id"] = course.id

        # verify if already exists an enrollment with this user_id and course_id
        if user.is_enrolled(alias=course.alias):
            return JsonResponse(
                data={"message": "This user is already enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create all access objects for the new user in the all materials of the course
        create_accesses_for_user(course=course, user=user)

        enrollment: EnrollmentSerializer = EnrollmentSerializer(data=request.data)

        if enrollment.is_valid():
            enrollment.save()
            return JsonResponse(
                data={"message": "Enrollment created successfully"},
                status=status.HTTP_201_CREATED,
            )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Course.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a course with this alias"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_enrollment_schema)
def get_enrollment(request, user_id: int, course_alias: str) -> JsonResponse:
    """
    View to get an enrollment by a user and course_alias
    Args:
        request: http request
        user_id: user's id to get his enrollment
        course_alias:  course's alias in which user is enrolled

    Returns:
        JsonResponse with enrollment information
    """
    try:
        course: Course = Course.objects.get(alias=course_alias)
        enrollment: Enrollment = Enrollment.objects.get(
            user_id=user_id, course_id=course.id
        )

        enrollment_serialized: EnrollmentSerializer = EnrollmentSerializer(enrollment)

        return JsonResponse(data=enrollment_serialized.data, status=status.HTTP_200_OK)

    except Course.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a course with this alias"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Enrollment.DoesNotExist:
        return JsonResponse(
            data={"message": "This user is not enrolled in this course"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@schema(schemas.appraise_course_schema)
def appraise_course(request, alias) -> JsonResponse:
    """
    View to appraise a course. Only enrolled users can appraise a course.

    Args:
        request: Json request with the following
        fields: stars and an optional comment
        alias (string): Course alias

    Returns:
        JsonResponse: Json response with a message and a status code
    """

    # Check required fields
    error_messages: dict = {}

    if "stars" not in request.data:
        error_messages["stars"] = "This field is required"
    elif request.data["stars"] not in range(0, 11):
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
        if request.data["comment"]:
            enrollment.appraisal_comment = request.data["comment"]

        old_appraisal_stars = enrollment.appraisal_stars
        enrollment.appraisal_stars = request.data["stars"]
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
    if request.data["comment"]:
        enrollment.appraisal_comment = request.data["comment"]

    enrollment.appraisal_stars = request.data["stars"]
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
