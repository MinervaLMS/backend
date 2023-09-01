from django.db import models
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from pytube import YouTube

from ..models import *
from ..schemas import *
from ..serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@schema(create_material_video_schema)
def create_material_video(request) -> JsonResponse:
    """
    View to upload a video for a material

    Args:
        request: http request with video data for creation, must be a youtube link

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    serializer = MaterialVideoSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "video was upload successfully"}, status=status.HTTP_201_CREATED)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@schema(get_material_schema)
def get_material_video(request, material_id: int) -> JsonResponse:
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
        materialVideo = MaterialVideo.objects.get(material_id=material_id)
        materialVideo = MaterialGetVideoSerializer(materialVideo)
        return JsonResponse(materialVideo.data, safe=False, status=status.HTTP_200_OK)
    except MaterialVideo.DoesNotExist:
        return JsonResponse({"message": "There is not a video material with that id"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
#@schema(update_material_schema)
def update_material_video(request, material_id: int) -> JsonResponse:
    """
    View to change material video url from a module in the database

    Args:
        request: request http with material data 
        material_id (int): material's id to update it

        {
            "external_id": "external_id"
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = MaterialVideo.objects.get(material_id=material_id)
    except MaterialVideo.DoesNotExist:
        return JsonResponse({"message": "There is not a material with that id"}, status=status.HTTP_404_NOT_FOUND)

    if 'length' in request.data:
        return JsonResponse({"message": "You can not change the length of a video manually"}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'source' in request.data:
        return JsonResponse({"message": "You can not change the source of a video manually"}, status=status.HTTP_400_BAD_REQUEST)

    for field_name, new_value in request.data.items():
        if hasattr(material, field_name):
            if field_name=="external_id":
                if not validlink(new_value):
                    return JsonResponse({"message": "The external_id should be a valid YouTube link"}, status=status.HTTP_400_BAD_REQUEST)
                length = video_length(new_value)
                setattr(material, "length", length)
            setattr(material, field_name, new_value)
        else:
            return JsonResponse({"message": f"{field_name} attribute does not exist in material"}, status=status.HTTP_400_BAD_REQUEST)

    
    material.save()
    serializer = MaterialVideoSerializer(material)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
#@schema(delete_material_schema)
def delete_material(request, material_video_id: int) -> JsonResponse:
    """
    Deletes video material video with passed id

    Args:
        request: http request
        material_id (int): material's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format,
    """

    try:
        material = MaterialVideo.objects.get(pk=material_video_id)

        material.delete()

        return JsonResponse({"message": "Material deleted successfully"}, status=status.HTTP_200_OK)
    except MaterialVideo.DoesNotExist:
        return JsonResponse({"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND)

def video_length(url):
        try:
            video = YouTube(url)
            length = video.length
            return length
        except Exception as e:
            return str(e)

def validlink(enlace):
        try:
            video = YouTube(enlace)
            return True
        except Exception:
            return False