from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.institution import Institution
from ..schemas import institution_schemas as schemas
from ..serializers.institution_serializer import InstitutionSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@schema(schemas.create_institution_schema)
def create_institution(request) -> JsonResponse:
    """
    View to create an institution

    Args:
        request: http request with institution data for creation

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = InstitutionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Institution was created successfully"},
            status=status.HTTP_201_CREATED,
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_institution_schema)
def get_institution(request, institution_id: int) -> JsonResponse:
    """
    View to get an institution

    Args:
        request: http request
        institution_id (int): institution id

    Returns:
        response (JsonResponse): HTTP response in JSON format
        with all institution information
    """

    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return JsonResponse(
            {"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = InstitutionSerializer(institution)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@schema(schemas.update_institution_schema)
def update_institution(request, institution_id: int) -> JsonResponse:
    """
    View to update an institution

    Args:
        request: http request
        institution_id (int): institution id

    Returns:
        response (JsonResponse): HTTP response in JSON format
        with all institution information
    """

    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return JsonResponse(
            {"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = InstitutionSerializer(institution, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Institution was updated successfully"},
            status=status.HTTP_200_OK,
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_institution_schema)
def delete_institution(request, institution_id: int) -> JsonResponse:
    """
    View to delete an institution

    Args:
        request: http request
        institution_id (int): institution id

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    try:
        institution = Institution.objects.get(id=institution_id)
    except Institution.DoesNotExist:
        return JsonResponse(
            {"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND
        )

    institution.delete()
    return JsonResponse(
        {"message": "Institution was deleted successfully"},
        status=status.HTTP_200_OK,
    )
