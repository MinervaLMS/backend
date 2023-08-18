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
from .models import Material, Module
from . import schemas

#TODO: Eliminar material (¿Eliminar o simplemnte añadir un campo para desactivarlo?)
#TODO: A view to edits material order must be created and it should not do in the materialChange view

@api_view(['POST'])
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

    serializer = MaterialSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Material created successfully"}, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(schemas.get_materials_by_module_schema)
def get_materials_by_module(request, module_id: int) -> JsonResponse:
    """
    Get all materials from a module in the database

    Args:
        request: request http 
        module_id (int): module's id to get all materials from it

    Returns:
        Json response with the fields of the serialized materials if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """
    try:
        Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There is not a module with that id"}, status=status.HTTP_404_NOT_FOUND)
    
    materials_by_module = Material.objects.filter(module_id=module_id).order_by('order')
    if not materials_by_module:
        return JsonResponse({"message": "There are not materials in this module"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MaterialSerializer(materials_by_module, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
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
        return JsonResponse({"message": "There is not a material with that id"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(schemas.update_material_order_schema)
def update_material_order(request, module_id: int) -> JsonResponse:
    """update materials order of a module

    Args:
        request : request http
        module_id (int): module's id to update order of its materials

        {
            material1_id: order, material2_id: order, material3_id: order
        }

    Returns:
        JsonResponse: _description_
    """
    
    try:
        Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There is not a module with that id"}, status=status.HTTP_404_NOT_FOUND)
    
    orders:list = list(request.data.values())
    orders.sort()
    correct_orders: list = [n for n in range(len(orders))]

    if orders != correct_orders:
        return JsonResponse({"message": "This materials order is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    

    materials = Material.objects.filter(module_id=module_id)
    for material in materials:
        material.order *= -1 
        material.save()
    
    for material in materials:
        material.order = request.data[str(material.id)]
        material.save()

    materials = MaterialSerializer(materials, many=True)

    return JsonResponse(materials.data, safe=False, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_material_schema)
def delete_material(request, material_id: int) -> JsonResponse:
    """
    Deletes material with passed id

    Args:
        request: http request
        material_id (int): material's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = Material.objects.get(pk=material_id)
        materials_ahead = Material.objects.filter(module_id=material.module_id, order__gt=material.order).order_by('order')
        material.order *= -1
        material.save()

        for material_ahead in materials_ahead:
            material_ahead.order -= 1
            material_ahead.save()

        material.delete()

        return JsonResponse({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except Material.DoesNotExist:
        return JsonResponse({"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND)