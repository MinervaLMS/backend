from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, schema

from ..schemas import user_schemas as schemas
from ..models.user import User
from ..serializers.user_serializer import UserSerializer
from courses.serializers.course_serializer import CourseEnrollmentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request) -> JsonResponse:
    """
    Get all users in the database, but only returns the UserSerializer
    fields ("email", "first_name", "last_name").

    Args:
        request: request http with user email

    Returns:
        Json response with the fields of the serialized users if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@schema(schemas.get_user_schema)
@permission_classes([IsAuthenticated])
def get_user(request, user_id) -> JsonResponse:
    """
    Get the user with the given id, but only returns the UserSerializer
    fields ("email", "first_name", "last_name").

    Args:
        request: request http with user email
        id: id of the user to get

    Returns:
        Json response with the fields of the serialized user if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@schema(schemas.get_user_courses_schema)
@permission_classes([IsAuthenticated])
def get_user_courses(request, user_id) -> JsonResponse:
    """
    Get the courses that the user is enrolled in, but only returns the
    CourseEnrollmentSerializer fields ("id", "name", "alias").

    Args:
        request: request http with user email
        email: email of the user to get

    Returns:
        Json response with the fields of the serialized courses if the user
        making the request is Authenticated, else throws 401 Unauthorized status
    """
    try:
        user = User.objects.get(pk=user_id)
        courses = user.courses.all()
        serializer = CourseEnrollmentSerializer(courses, many=True)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)

    return JsonResponse(serializer.data, safe=False)
