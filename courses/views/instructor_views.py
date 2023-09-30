from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.instructor import Instructor
from ..models.course import Course
from accounts.models.user import User

from ..serializers.instructor_serializer import InstructorSerializer
from ..schemas import instructor_schemas as schemas


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@schema(schemas.create_instructor_schema)
def create_instructor(request) -> JsonResponse:
    """Create a new instructor
    Args:
        request: request http with data to create a new instructor

    Returns:
        JsonResponse with confirmation message
    """
    try:
        User.objects.get(pk=request.data["user_id"])
        Course.objects.get(pk=request.data["course_id"])

        # verify if instructor_type is valid
        if request.data["instructor_type"] not in ["E", "T", "A"]:
            return JsonResponse(
                data={"message": "Invalid instructor type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # verify if already exists an instructor with this user_id and course_id
        if Instructor.objects.filter(
            user_id=request.data["user_id"], course_id=request.data["course_id"]
        ).exists():
            return JsonResponse(
                data={"message": "This user is already instructor in this course"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instructor: InstructorSerializer = InstructorSerializer(data=request.data)
        if instructor.is_valid():
            instructor.save()
            return JsonResponse(
                data={"message": "Instructor created successfully"},
                status=status.HTTP_201_CREATED,
            )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Course.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a course with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_instructor_schema)
def get_instructor(request, user_id: int, course_id: int) -> JsonResponse:
    """Get an instructor by user_id and course_id

    Args:
        request: http request
        user_id: user's id to get instructor
        course_id: course's id to get instructor

    Returns:
        JsonResponse with instructor's data
    """
    try:
        instructor: Instructor = Instructor.objects.get(
            user_id=user_id, course_id=course_id
        )
        instructor_serializer: InstructorSerializer = InstructorSerializer(instructor)

        return JsonResponse(data=instructor_serializer.data, status=status.HTTP_200_OK)

    except Instructor.DoesNotExist:
        return JsonResponse(
            data={
                "message": "There is not an instructor with this user_id and course_id"
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@schema(schemas.update_instructor_type_schema)
def update_instructor_type(request, user_id: int, course_id: int) -> JsonResponse:
    """Update an instructor by user_id and course_id

    Args:
        request: http request with new type of instructor
        user_id: user's id to get instructor
        course_id: course's id to get instructor

    Returns:
        JsonResponse with confirmation message
    """
    try:
        instructor: Instructor = Instructor.objects.get(
            user_id=user_id, course_id=course_id
        )

        # verify if instructor_type is valid
        if request.data["instructor_type"] not in ["E", "T", "A"]:
            return JsonResponse(
                data={"message": "Invalid instructor type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instructor.instructor_type = request.data["instructor_type"]
        instructor.save(update_fields=["instructor_type"])
        return JsonResponse(
            data={"message": "Instructor updated successfully"},
            status=status.HTTP_200_OK,
        )

    except Instructor.DoesNotExist:
        return JsonResponse(
            data={
                "message": "There is not an instructor with this user_id and course_id"
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_instructor_schema)
def delete_instructor(request, user_id: int, course_id: int) -> JsonResponse:
    """View to delete an instructor by user_id and course_id

    Args:
        request: http request
        user_id: user's id to delete instructor
        course_id: course's id to delete instructor

    Returns:
        JsonResponse with confirmation message
    """
    try:
        instructor: Instructor = Instructor.objects.get(
            user_id=user_id, course_id=course_id
        )
        instructor.delete()

        return JsonResponse(
            data={"message": "Instructor deleted successfully"},
            status=status.HTTP_200_OK,
        )

    except Instructor.DoesNotExist:
        return JsonResponse(
            data={
                "message": "There is not an instructor with this user_id and course_id"
            },
            status=status.HTTP_404_NOT_FOUND,
        )
