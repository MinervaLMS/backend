from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from .serializers import CourseSerializer
from .models import Course
from . import schemas

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