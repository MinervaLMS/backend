from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..schemas import *
from ..serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@schema(create_module_schema)
def create_module(request) -> JsonResponse:
    """
    View to create a new module from a course in the database

    Args:
        request: request http with module data
            course_id
            name
            order
    Returns:
        response (JsonResponse): HTTP response in JSON format, 400 if the validation was wrong
    """

    serializer = ModuleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Module created successfully"}, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(get_module_schema)
def get_module_by_id(request, module_id: int) -> JsonResponse:
    """
    Get module by its id

    Args:
        request: request http
        module_id (int): module's id to get it

    Returns:
        Json response with the fields of the serialized module if the user making
        the request is Authenticated, else throws 401 Unauthorized status or 404 if module does not exist
    """

    try:
        module = Module.objects.get(id=module_id)
        module = ModuleSerializer(module)
        return JsonResponse(module.data, safe=False, status=status.HTTP_200_OK)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There is not a module with that id"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(update_module_schema)
def update_module(request, module_id: int) -> JsonResponse:
    '''
    View to change module data from a course in the database

    Args:
        request: request http with module data
        module_id (int): module's id to update it

        {
            "name": "Nombre",
        }
    '''

    try:
        module = Module.objects.get(id=module_id)
    except Module.objects.get(id=module_id).DoesNotExist:
        return JsonResponse({"message": "There is not a module with that id"}, status=status.HTTP_404_NOT_FOUND)

    if "name" in request.data:
        module.name = request.data['name']
    else:
        return JsonResponse({"message": "You must provide a name"}, status=status.HTTP_400_BAD_REQUEST)

    module.save()
    serializer = ModuleSerializer(module)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(delete_module_schema)
def delete_module(request, module_id: int) -> JsonResponse:
    """
    Deletes module with passed id

    Args:
        request: http request
        module_id (int): module's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        module = Module.objects.get(pk=module_id)
        modules_ahead = Module.objects.filter(
            course_id=module.course_id, order__gt=module.order).order_by('order')
        module.order *= -1
        module.save()

        for module_ahead in modules_ahead:
            module_ahead.order -= 1
            module_ahead.save()

        module.delete()

        return JsonResponse({"message": "Module deleted successfully"}, status=status.HTTP_200_OK)
    except Module.DoesNotExist:
        return JsonResponse({"message": "Module does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(get_materials_by_module_schema)
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

    materials_by_module = Material.objects.filter(
        module_id=module_id).order_by('order')

    if not materials_by_module:
        return JsonResponse({"message": "There are not materials in this module"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MaterialSerializer(materials_by_module, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(get_material_by_module_order_schema)
def get_material_by_module_order(request, module_id: str, order: int) -> JsonResponse:
    """
    Get a module from a course in the database

    Args:
        request: request http
        module_id (str): Id of the module
        order (int): Order of the module

    Returns:
        Json response with the fields of the serialized materials if the user making
        the request is Authenticated, else throws 401 Unauthorized status. If there is no course
        or module order, then throws 404 status
    """

    try:
        module = Course.objects.get(pk=module_id)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There is not a module with that id"}, status=status.HTTP_404_NOT_FOUND)

    try:
        material_by_module = Material.objects.get(
            module_id=module.id, order=order)
        material_by_module = MaterialSerializer(material_by_module)
        return JsonResponse(material_by_module.data, safe=False, status=status.HTTP_200_OK)
    except Material.DoesNotExist:
        return JsonResponse({"message": "This module has not a material in this order"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(update_material_order_schema)
def update_material_order(request, module_id: int) -> JsonResponse:
    """Update materials order of a module

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

    orders: list = list(request.data.values())
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
