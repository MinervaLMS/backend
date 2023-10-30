from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated

from ..models.module import Module
from ..models.material import Material
from ..schemas import material_schemas as schemas
from ..serializers.material_serializer import MaterialSerializer
from ..helpers.module_material_counts import (
    update_count_created_material,
    update_count_deleted_material,
    update_count_updated_material,
)
from ..helpers.create_all_accesses import create_accesses_for_material


@api_view(["POST"])
@schema(schemas.create_material_schema)
@permission_classes([IsAuthenticated])
def create_material(request) -> JsonResponse:
    """
    View to create a new material from a module in the database

    Args:
        request: request http with material data

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    material: Material | None = None
    try:
        module: Module = Module.objects.get(id=request.data.get("module_id"))

        serializer = MaterialSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            material = serializer.save()
            # Update module's material counts
            update_count_created_material(serializer=serializer)
            # Create all access objects for the new material
            # TODO: Doing the same thing when a enrollment is created
            create_accesses_for_material(
                course_id=module.course_id.id, material=material
            )
            response = serializer.data
            response["message"] = "Material created successfully"
            return JsonResponse(response, status=status.HTTP_201_CREATED)

    except serializers.ValidationError as exc:
        return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
    # return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

    except Module.DoesNotExist:
        return JsonResponse(
            data={"message": "There is not a module with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_material_schema)
def get_material(request, material_id: int) -> JsonResponse:
    """
    Get material by its id

    Args:
        request: request http
        material_id (int): material's id to get it

    Returns:
        Json response with the fields of the serialized material if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    try:
        material = Material.objects.get(id=material_id)
        material = MaterialSerializer(material)
        return JsonResponse(material.data, safe=False, status=status.HTTP_200_OK)
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@schema(schemas.update_material_schema)
def update_material(request, material_id: int) -> JsonResponse:
    """
    View to change material data from a module in the database

    Args:
        request: request http with material data
        material_id (int): material's id to update it

        {
            "name": "Nuevo nombre",
            "material_type": "Nuevo tipo",
            "is_extra": boolean
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = Material.objects.get(id=material_id)
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if "order" in request.data:
        return JsonResponse(
            {"message": "You can not change the order of a material through this url"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Store old material properties before they are changed
    request_data = request.data
    old_material_type = material.material_type
    old_is_extra = material.is_extra

    for field_name, new_value in request_data.items():
        if hasattr(material, field_name):
            setattr(material, field_name, new_value)
        else:
            return JsonResponse(
                {"message": f"{field_name} attribute does not exist in material"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    material.save()

    # update module's material counts

    if (
        request_data.get("material_type") is not None
        or request_data.get("is_extra") is not None
    ):
        update_count_updated_material(
            material=material,
            old_material_type=old_material_type,
            old_is_extra=old_is_extra,
            new_material_type=request_data.get("material_type"),
            new_is_extra=request_data.get("is_extra"),
        )

    serializer = MaterialSerializer(material)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_material_schema)
def delete_material(request, material_id: int) -> JsonResponse:
    """
    Deletes material with passed id

    Args:
        request: http request
        material_id (int): material's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format,
    """

    try:
        material = Material.objects.get(pk=material_id)
        materials_ahead = Material.objects.filter(
            module_id=material.module_id, order__gt=material.order
        ).order_by("order")
        material.order = -material.order if material.order > 0 else -1
        material.save()

        for material_ahead in materials_ahead:
            material_ahead.order -= 1
            material_ahead.save()

        # Update module's material counts
        update_count_deleted_material(material=material)

        material.delete()

        return JsonResponse(
            {"message": "Material deleted successfully"}, status=status.HTTP_200_OK
        )
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
