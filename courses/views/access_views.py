from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.material import Material
from ..models.access import Access
from accounts.models.user import User
from ..serializers.access_serializer import AccessSerializer
from ..helpers.enrollment_validate import validate_enrollemet


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_access(request) -> JsonResponse:
    """Create a new access to a material by a user

    Args:
        request: request http with access data
        {
            "material_id": int,
            "user_id": int
        }

    Returns:
        JsonResponse: HTTP response in JSON format
    """
    try:
        user: User = User.objects.get(id=request.data["user_id"])
        material: Material = Material.objects.get(id=request.data["material_id"])
        # Verify if the user is enrolled in the course to which the material belongs
        if not validate_enrollemet(user.id, material.id):
            return JsonResponse(
                {"message": "You do not have permission to access this material"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = AccessSerializer(data=request.data)
        if access.is_valid():
            access.save()
            return JsonResponse(
                {"message": "Access created successfully"},
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(access.errors, status=status.HTTP_400_BAD_REQUEST)

    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_access(request, material_id: int, user_id: int) -> JsonResponse:
    """Get access by its material and user

    Args:
        request: request http
        material_id (int): material's id to get it
        user_id (int): user's id to get it

    Returns:
        JsonResponse: HTTP response in JSON format
    """
    try:
        access = Access.objects.get(material_id=material_id, user_id=user_id)
        access = AccessSerializer(access)
        return JsonResponse(access.data, safe=False, status=status.HTTP_200_OK)

    except Access.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an access with that material and user"},
            status=status.HTTP_404_NOT_FOUND,
        )


# TODO: Se están sumando likes y restando dislikes cuando se actualiza el like
# TODO: Crear función accerder a material y retorna el acceso
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def assess_material(request) -> JsonResponse:
    """View to add a like to a material
    Args:
        request: request http with material data
        {
            "material_id": int,
            "user_id": int,
            "like": bool
        }

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        user: User = User.objects.get(id=request.data["user_id"])
        material: Material = Material.objects.get(id=request.data["material_id"])
        # Verify if the user is enrolled in the course to which the material belongs
        if not validate_enrollemet(user.id, material.id):
            return JsonResponse(
                {"message": "You do not have permission to assess this material"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Update the like field
        access = Access.objects.get(material_id=material.id, user_id=user.id)
        access.like = request.data["like"]
        # Then update the material's likes
        if access.like is None:  # If the user has not assessed the material yet
            if request.data["like"]:
                material.likes += 1
            else:
                material.dislikes += 1
        else:
            if request.data["like"]:
                material.likes += 1
                material.dislikes -= 1
            else:
                material.likes -= 1
                material.dislikes += 1
        access.save()
        material.save()

        return JsonResponse(
            {"message": "Access assessed successfully"}, status=status.HTTP_201_CREATED
        )

    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a user with this id"},
            status=status.HTTP_404_NOT_FOUND,
        )
