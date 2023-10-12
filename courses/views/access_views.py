from django.http import JsonResponse
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.material import Material
from ..models.access import Access
from accounts.models.user import User
from ..schemas import access_schemas as schemas
from ..serializers.access_serializer import AccessSerializer
from ..helpers.enrollment_validate import validate_enrollment


@api_view(["POST"])
@schema(schemas.create_access_schema)
@permission_classes([IsAuthenticated])
def create_access(request) -> JsonResponse:
    """Create new access to a material by a user, if the user has not accessed
    the material before. But if the user has accessed the material before,
    update the access data such as views and last_view

    Args:
        request: request http with access data
        {
            "material_id": int,
            "user_id": int
        }

    Returns:
        JsonResponse: HTTP response in JSON format with the access data
    """
    try:
        user: User = User.objects.get(id=request.data["user_id"])
        material: Material = Material.objects.get(id=request.data["material_id"])
        # Verify if the user is enrolled in the course to which the material belongs
        if not validate_enrollment(user.id, material.id):
            return JsonResponse(
                {"message": "You do not have permission to access this material"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Verify if the user has accessed the material before
        access: Access = Access.objects.filter(
            material_id=material.id, user_id=user.id
        ).first()
        if access:
            access.views += 1
            access.last_view = timezone.now()
            access.save(update_fields=["views", "last_view"])
            access = AccessSerializer(access)
            return JsonResponse(
                access.data,
                safe=False,
                status=status.HTTP_200_OK,
            )

        # If the user has not accessed the material before, create a new access
        access = AccessSerializer(data=request.data)
        if access.is_valid():
            access.save()
            return JsonResponse(
                access.data,
                safe=False,
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
@schema(schemas.get_access_schema)
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


@api_view(["PATCH"])
@schema(schemas.update_access_like_schema)
@permission_classes([IsAuthenticated])
def update_access_like(request) -> JsonResponse:
    """View to add a like to a material
    Args:
        request: request http with material data
        {
            "material_id": int,
            "user_id": int
        }

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        # Verify if user has access to the material before
        access: Access = Access.objects.get(
            material_id=request.data["material_id"], user_id=request.data["user_id"]
        )
        material: Material = access.material_id
        # Verify if the user has assessed the material or not
        if access.like is None:
            # If the user has not assessed the material, add a like
            material.likes += 1
            access.like = True
        else:
            if access.like:
                # If the user has liked the material before, remove the like
                material.likes -= 1
                access.like = None
            else:
                material.likes += 1
                material.dislikes -= 1
                access.like = True
        # Update the like field
        material.save(update_fields=["likes", "dislikes"])
        access.save(update_fields=["like"])
        return JsonResponse(
            {"message": "Access assessed successfully"}, status=status.HTTP_200_OK
        )

    except Access.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an access with that material and user"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PATCH"])
@schema(schemas.update_access_completed_schema)
@permission_classes([IsAuthenticated])
def update_access_completed(request) -> JsonResponse:
    """view to make an access appear as completed
    Args:
        request: request http with material data
        {
            "material_id": int,
            "user_id": int
        }

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        # Verify if user has access to the material before
        access: Access = Access.objects.get(
            material_id=request.data["material_id"], user_id=request.data["user_id"]
        )
        # Verify if the user has completed the material or not
        if access.completed is None:
            # If the user has not completed the material,
            # turn completed field into "True"
            access.completed = True
        else:
            # If the user has completed the material before,
            # turn completed field into Null
            access.completed = None
            access.save(update_fields=["completed"])
            return JsonResponse(
                {"message": "Access completed eliminated"}, status=status.HTTP_200_OK
            )
        # Update the completed field
        access.save(update_fields=["completed"])
        return JsonResponse(
            {"message": "Access completed successfully"}, status=status.HTTP_200_OK
        )

    except Access.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an access with that material and user"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PATCH"])
@schema(schemas.update_access_dislike_schema)
@permission_classes([IsAuthenticated])
def update_access_dislike(request) -> JsonResponse:
    """View to add a dislike to a material
    Args:
        request: request http with material data
        {
            "material_id": int,
            "user_id": int
        }

    Returns:
        JsonResponse (JsonResponse): HTTP response in JSON format
    """
    try:
        # Verify if user has access to the material before
        access: Access = Access.objects.get(
            material_id=request.data["material_id"], user_id=request.data["user_id"]
        )
        material: Material = access.material_id
        # Verify if the user has assessed the material or not
        if access.like is None:
            # If the user has not assessed the material, add a dislike
            material.dislikes += 1
            access.like = False
        else:
            if access.like:
                # If the user has liked the material before, remove the like
                material.likes -= 1
                material.dislikes += 1
                access.like = False
            else:
                material.dislikes -= 1
                access.like = None
        material.save(update_fields=["likes", "dislikes"])
        access.save(update_fields=["like"])

        return JsonResponse(
            {"message": "Access assessed successfully"}, status=status.HTTP_200_OK
        )

    except Access.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an access with that material and user"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
@schema(schemas.delete_access_schema)
@permission_classes([IsAuthenticated])
def delete_access(request, material_id: int, user_id: int) -> JsonResponse:
    """View to delete access to a material by a user

    Args:
        request : request http
        material_id (int): material's id to which the access belongs
        user_id (int): user's id to which the access belongs

    Returns:
        JsonResponse: HTTP response in JSON format
    """

    try:
        access = Access.objects.get(material_id=material_id, user_id=user_id)
        access.delete()
        return JsonResponse(
            {"message": "Access deleted successfully"}, status=status.HTTP_200_OK
        )

    except Access.DoesNotExist:
        return JsonResponse(
            {"message": "There is not an access with that material and user"},
            status=status.HTTP_404_NOT_FOUND,
        )


# TODO: These views below only will be used to help the front-end
@api_view(["POST"])
# @schema(schemas.delete_access_schema)
@permission_classes([IsAuthenticated])
def create_all_access_to_user(request) -> JsonResponse:
    """View to create all accesses to a user in materials of specific module

    Args:
        request : request http
        user_id (int): user's id to which the access belongs
        module_id (int): module's id to which materials belong
        {
            "user_id": int,
            "module_id": int
        }

    Returns:
        JsonResponse: HTTP response in JSON format
    """
    try:
        user: User = User.objects.get(id=request.data["user_id"])
        materials: list[Material] = Material.objects.filter(
            module_id=request.data["module_id"]
        )
        accesses: list[Access] = []
        for material in materials:
            access = Access(user_id=user, material_id=material)
            accesses.append(access)
        Access.objects.bulk_create(accesses)

        return JsonResponse(
            {"message": "Accesses created successfully"}, status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a user with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accesses_by_user(request, user_id: int, module_id: int) -> JsonResponse:
    """View to get all accesses by a user in materials of specific module

    Args:
        request : request http
        user_id (int): user's id to which the access belongs
        module_id (int): module's id to which materials belong

    Returns:
        JsonResponse: HTTP response in JSON format
    """
    try:
        user: User = User.objects.get(id=user_id)
        materials: list[Material] = Material.objects.filter(module_id=module_id)
        accesses: list[Access] = Access.objects.filter(
            material_id__in=materials, user_id=user
        )
        accesses = AccessSerializer(accesses, many=True)
        return JsonResponse(accesses.data, safe=False, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a user with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
