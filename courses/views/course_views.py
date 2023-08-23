from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..schemas import *
from ..serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@schema(create_course_schema)
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
@schema(get_course_schema)
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
@schema(update_course_schema)
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
@schema(delete_course_schema)
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(get_modules_by_course_schema)
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
@schema(get_module_by_course_order_schema)
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
        module_by_course = Module.objects.get(course_id=course.id, order=order)
        module_by_course = ModuleSerializer(module_by_course)

        return JsonResponse(module_by_course.data, safe=False, status=status.HTTP_200_OK)
    except Module.DoesNotExist:
        return JsonResponse({"message": "There are not modules by this order"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@schema(update_module_order_schema)
def update_module_order(request, alias: str) -> JsonResponse:
    """update modules order of a course

    Args:
        request : request http
        course_id (int): course's alias to update order of its modules

        {
            module1_id: order1,
            module2_id: order2,
            module3_id: order3,
            ...
        }

    Returns:
        JsonResponse: Return data of the modules of the course_id with order modified
    """

    try:
        course = Course.objects.get(alias=alias)
    except Course.DoesNotExist:
        return JsonResponse({"message": "There is not a course with that id"}, status=status.HTTP_404_NOT_FOUND)

    orders: list = list(request.data.values())
    orders.sort()
    correct_orders: list = [n for n in range(len(orders))]

    if orders != correct_orders:
        return JsonResponse({"message": "This modules order is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    modules = Module.objects.filter(course_id=course.id)

    for module in modules:
        module.order *= -1
        module.save()

    for module in modules:
        module.order = request.data[str(module.id)]
        module.save()

    modules = ModuleSerializer(modules, many=True)

    return JsonResponse(modules.data, safe=False, status=status.HTTP_200_OK)
