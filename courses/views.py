from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from collections import defaultdict

from .serializers import MaterialSerializer
from .models import Material
from . import schemas

#TODO: Eliminar material (¿Eliminar o simplemnte añadir un campo para desactivarlo?)
#TODO: A views to edits material order must be created and it should not do in the materialChange view

@api_view(['POST'])
@schema(schemas.postMaterial_schema)
@permission_classes([IsAuthenticated])
def postMaterial_view(request) -> JsonResponse:
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
def material_list(request) -> JsonResponse:
    """
    Get all materials in the database ordered by module_id and order.

    Args:
        request: request http 

    Returns:
        Json response with the fields of the serialized materials if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """

    materials_by_module = Material.objects.all().order_by('module_id', 'order')

    serializer = MaterialSerializer(materials_by_module, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@schema(schemas.editMaterial_schema)
def materialChange(request, material_id) -> JsonResponse:
    """
    View to change material data from a module in the database

    Args:
        In the url must be the id of the material
        request: request http with material data for post it
        Here is an example of how has to be Json request data:
        {
        "fields_to_update": {
            "name": "Nuevo nombre",
            "material_type": "Nuevo tipo"
            }
        }

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = Material.objects.get(id=material_id)
    except Material.DoesNotExist:
        return JsonResponse({"message": "There is not a material with that id"}, status=status.HTTP_404_NOT_FOUND)
    
    fields_to_update = request.data.get('fields_to_update', {})

    for field_name, new_value in fields_to_update.items():
        if hasattr(material, field_name):
            setattr(material, field_name, new_value)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

    material.save()
    serializer = MaterialSerializer(material)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_material_schema)
def delete_material_view(request, material_id: int) -> JsonResponse:
    """
    Deletes material with passed id

    Args:
        request: http request
        material_id: material's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = Material.objects.get(pk=material_id)
        material.delete()
        return JsonResponse({"message": f"Material with id:{material_id} deletes successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Material.DoesNotExist:
        return JsonResponse({"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND)