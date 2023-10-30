from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, schema

from ioc.models import IoCodeSubmissionSummary
from ioc.serializers.IoCodeSubmissionSummarySerializer import IoCodeSubmissionSummarySerializer
from ..models.user import User
from courses.models import Material, Access
from ..serializers.user_serializer import UserSerializer
from courses.serializers.access_serializer import AccessSerializer
from courses.serializers.material_serializer import MaterialSerializer
from ..schemas import user_schemas as schemas
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


@api_view(["GET"])
@schema(schemas.get_user_materials_schema)
@permission_classes([IsAuthenticated])
def get_user_materials(request, user_id: int, module_id: int) -> JsonResponse:
    """
    Get the materials that the user has accessed to in a module
    Args:
        request: request http
        user_id: User's id who has accessed to the materials
        module_id: Module's id which materials belongs to

    Returns:
        Json response with materials data
    """
    try:
        user: User = User.objects.get(id=user_id)
        materials: list[Material] = list(
            user.materials.filter(module_id=module_id).order_by("order")
        )

        if not materials:
            return JsonResponse(
                data={"message": "There are not materials in this module"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_materials = MaterialSerializer(materials, many=True)

        for serialized_material in serialized_materials.data:
            material = materials.pop(0)
            access: Access = material.access_set.filter(user_id=user_id).first()
            access_data = AccessSerializer(access).data
            if str(material.material_type).upper() == "IOC":
                summary: IoCodeSubmissionSummary = material.submission_summary.filter(
                    user_id=user_id
                ).first()
                access_data["summary"] = IoCodeSubmissionSummarySerializer(summary).data

            serialized_material["access"] = access_data

        return JsonResponse(
            data=serialized_materials.data, safe=False, status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a user with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )
