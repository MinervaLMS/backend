from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from . import schemas

# TODO: Eliminar material (¿Eliminar o simplemnte añadir un campo para desactivarlo?)
# TODO: A view to edits material order must be created and it should not do in the materialChange view


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@schema(schemas.create_course_schema)
def create_course(request) -> JsonResponse:
    """
    View to create a course

    Args:
        request: http request with course data for creation

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Course was created successfully"}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(schemas.get_course_schema)
def get_course(request, alias: str) -> JsonResponse:
    """
    View to get a course

    Args:
        request: http request
        alias (str): course alias

    Returns:
        response (JsonResponse): HTTP response in JSON format with all course information
    """

    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(schemas.update_course_schema)
def update_course(request, alias: str) -> JsonResponse:
    """
    View to update a course

    Args:
        request: http request with course fields to update
        alias (str): course alias

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Course was changed successfully"}, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_course_schema)
def delete_course(request, alias: str) -> JsonResponse:
    """
    View to delete a course

    Args:
        request: http request
        alias (str): course alias

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    course.delete()
    return JsonResponse({"message": "Course was deleted successfully"}, status=status.HTTP_200_OK)


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

    materials_by_module = Material.objects.filter(
        module_id=module_id).order_by('order')
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

# Modules


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@schema(schemas.create_module_schema)
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
@schema(schemas.get_module_schema)
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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_module_schema)
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(schemas.update_module_order_schema)
def update_module_order(request, course_id: int) -> JsonResponse:
    """update modules order of a course

    Args:
        request : request http
        course_id (int): course's id to update order of its modules

        {
            module1_id: order, module2_id: order, module3_id: order
        }

    Returns:
        JsonResponse: Return data of the modules of the course_id with order modified
    """

    try:
        Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"message": "There is not a course with that id"}, status=status.HTTP_404_NOT_FOUND)

    orders: list = list(request.data.values())
    orders.sort()
    correct_orders: list = [n for n in range(len(orders))]

    if orders != correct_orders:
        return JsonResponse({"message": "This modules order is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    modules = Module.objects.filter(course_id=course_id)
    for module in modules:
        module.order *= -1
        module.save()

    for module in modules:
        module.order = request.data[str(module.id)]
        module.save()

    modules = ModuleSerializer(modules, many=True)

    return JsonResponse(modules.data, safe=False, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(schemas.update_module_schema)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(schemas.get_modules_by_course_schema)
def get_modules_by_course(request, alias: str) -> JsonResponse:
    """
    Get all modules from a course in the database

    Args:
        request: request http 
        alias (str): Alias to get all modules from it

    Returns:
        Json response with the fields of the serialized materials if the user making
        the request is Authenticated, else throws 401 Unauthorized status
    """
    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"message": "There is not a course with that id"}, status=status.HTTP_404_NOT_FOUND)
    modules_by_course = Module.objects.filter(
        course_id=course.id).order_by('order')
    if not modules_by_course:
        return JsonResponse({"message": "There are not modules in this course"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ModuleSerializer(modules_by_course, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(schemas.get_module_by_course_order_schema)
def get_module_by_course_order(request, alias: str, order: int) -> JsonResponse:
    """
    Get a module from a course in the database

    Args:
        request: request http 
        alias (str): Alias to get all modules from it
        order (int): Order of the module

    Returns:
        Json response with the fields of the serialized materials if the user making
        the request is Authenticated, else throws 401 Unauthorized status. If there is no course
        or module order, then throws 404 status
    """
    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"message": "There is not a course with that id"}, status=status.HTTP_404_NOT_FOUND)
    try:
        module_by_course = Module.objects.get(
            course_id=course.id, order=order)
        module_by_course = ModuleSerializer(module_by_course)
        return JsonResponse(module_by_course.data, safe=False, status=status.HTTP_200_OK)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There are not modules by this order"}, status=status.HTTP_404_NOT_FOUND)
