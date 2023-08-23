from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..schemas import *
from ..serializers import *


@api_view(['POST'])
@schema(create_material_schema)
@permission_classes([IsAuthenticated])
def create_material(request) -> JsonResponse:
    """
    View to create a new material from a module in the database

    Args:
        request: request http with material data

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = MaterialSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Material created successfully"}, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(get_material_schema)
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
        return JsonResponse({"message": "There is not a material with that id"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(update_material_schema)
def update_material(request, material_id: int) -> JsonResponse:
    """
    View to change material data from a module in the database

    Args:
        request: request http with material data 
        material_id (int): material's id to update it

        {
            "name": "Nuevo nombre",
            "material_type": "Nuevo tipo"
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = Material.objects.get(id=material_id)
    except Material.DoesNotExist:
        return JsonResponse({"message": "There is not a material with that id"}, status=status.HTTP_404_NOT_FOUND)

    if 'order' in request.data:
        return JsonResponse({"message": "You can not change the order of a material through this url"}, status=status.HTTP_400_BAD_REQUEST)

    for field_name, new_value in request.data.items():
        if hasattr(material, field_name):
            setattr(material, field_name, new_value)
        else:
            return JsonResponse({"message": f"{field_name} attribute does not exist in material"}, status=status.HTTP_400_BAD_REQUEST)

    material.save()
    serializer = MaterialSerializer(material)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(delete_material_schema)
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
            module_id=material.module_id, order__gt=material.order).order_by('order')
        material.order *= -1
        material.save()

        for material_ahead in materials_ahead:
            material_ahead.order -= 1
            material_ahead.save()

        material.delete()

        return JsonResponse({"message": "Material deleted successfully"}, status=status.HTTP_200_OK)
    except Material.DoesNotExist:
        return JsonResponse({"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND)
