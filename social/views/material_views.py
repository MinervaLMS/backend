from django.http import JsonResponse
from django.db.models.expressions import RawSQL

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from courses.models.material import Material
from courses.models.course import Course
from courses.models.enrollment import Enrollment


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def like_materail(request, material_id: int, user_id: int) -> JsonResponse:
    """View to add a like to a material
    Args:
        request: request http
        material_id (int): material's id to like it
        user_id (int): user's id that likes the material

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        material = Material.objects.get(id=material_id)
        # Query to get the course that material belongs to
        query: str = (
            "SELECT course_id_id FROM courses_module "
            "INNER JOIN courses_material ON courses_material.module_id_id "
            "= courses_module.id WHERE courses_material.id = %s"
        )
        course = Course.objects.filter(id=RawSQL(query, (material.id,))).first()
        # Verify if the user has permission to give a like to the material
        if Enrollment.objects.filter(user_id=user_id, course_id=course).exists():
            material.likes += 1
            material.save()
            return JsonResponse(
                {"message": "Like given successfully"},
                safe=False,
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            {"message": "You do not have permission to give a like to this material"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def dislike_materail(request, material_id: int, user_id: int) -> JsonResponse:
    """View to add a dislike to a material
    Args:
        request: request http
        material_id (int): material's id to dislike it
        user_id (int): user's id that dislikes the material

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        material = Material.objects.get(id=material_id)
        # Query to get the course that material belongs to
        query: str = (
            "SELECT course_id_id FROM courses_module "
            "INNER JOIN courses_material ON courses_material.module_id_id "
            "= courses_module.id WHERE courses_material.id = %s"
        )
        course = Course.objects.filter(id=RawSQL(query, (material.id,))).first()
        # Verify if the user has permission to give a dislike to the material
        if Enrollment.objects.filter(user_id=user_id, course_id=course).exists():
            material.dislikes += 1
            material.save()
            return JsonResponse(
                {"message": "Dislike given successfully"},
                safe=False,
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            {"message": "You do not have permission to give a like to this material"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
