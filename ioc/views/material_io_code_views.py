from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from ..models.material_io_code import MaterialIoCode


from ..serializers.material_io_code_serializer import (
    MaterialGetIoCodeSerializer,
    MaterialIoCodeSerializer
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
# @schema(schemas.create_material_io_code_schema)
def create_material_io_code(request) -> JsonResponse:
    """
    Args:
        request: http request with max_time and max_memory data

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    serializer = MaterialIoCodeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Imput and output code was upload successfully"}, status=status.HTTP_201_CREATED
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
# @schema(schemas.get_material_io_code_schema)
def get_material_io_code(request, material_id: int) -> JsonResponse:
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
        materialIoCode = MaterialIoCode.objects.get(material_id=material_id)
        materialIoCode = MaterialGetIoCodeSerializer(materialIoCode)
        return JsonResponse(materialIoCode.data, safe=False, status=status.HTTP_200_OK)
    except MaterialIoCode.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a Io_Code with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
# @schema(schemas.update_material_io_code_schema)
def update_material_io_code(request, material_id: int) -> JsonResponse:
    """
    View to change material input-output video from a exercise in the database

    Args:
        request: request http with material data
        material_id (int): material's id to update it

        {
            "id": "id"
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        material = MaterialIoCode.objects.get(material_id=material_id)
    except MaterialIoCode.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if "max_time" in request.data:
        material.max_time = request.data["max_time"]
        
    if "max_memory" in request.data:
        material.max_memory = request.data["max_memory"]
    
    material.save()
    serializer = MaterialIoCodeSerializer(material)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
# @schema(schemas.delete_material_io_code_schema)
def delete_material(request, material_io_code_id: int) -> JsonResponse:
    """
    Deletes input-output code with passed id

    Args:
        request: http request
        material_id (int): material's id to be removed

    Returns:
        response (JsonResponse): HTTP response in JSON format,
    """

    try:
        material = MaterialIoCode.objects.get(pk=material_io_code_id)

        material.delete()

        return JsonResponse(
            {"message": "Material deleted successfully"}, status=status.HTTP_200_OK
        )
    except MaterialIoCode.DoesNotExist:
        return JsonResponse(
            {"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND
        )