from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.material import Material
from ..models.material_html import MaterialHTML
from ..schemas import material_html_schemas as schemas
from ..serializers.material_html_serializer import MaterialHTMLSerializer


@api_view(["POST"])
@schema(schemas.create_material_html_schema)
@permission_classes([IsAuthenticated])
def create_material_html(request) -> JsonResponse:
    """
    View to create a new material html content from a
    material in the database with material_type = 'HTML'

    Args:
        request: request http with material html data

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = MaterialHTMLSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "HTML Material created successfully"},
            status=status.HTTP_201_CREATED,
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@schema(schemas.get_material_html_schema)
def get_material_html(request, material_id: int) -> JsonResponse:
    """
    Get material HTML content by its material ID

    Args:
        request: request http
        material_id (int): material's id to get it

    Returns:
        Json response with the HTML content of the material
    """

    try:
        material = Material.objects.get(id=material_id)
        material_html = MaterialHTML.objects.get(material_id=material.id)
        material_content = MaterialHTMLSerializer(material_html)

        return JsonResponse(
            material_content.data, safe=False, status=status.HTTP_200_OK
        )
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except MaterialHTML.DoesNotExist:
        return JsonResponse(
            {"message": "This material does not have HTML content"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@schema(schemas.update_material_html_schema)
def update_material_html(request, material_id: int) -> JsonResponse:
    """
    View to change material HTML content from a material in the database

    Args:
        request: request http with material HTML content
        material_id (int): material's id to update its HTML content

        {
            "content": "..."
        }
    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    if "content" not in request.data:
        return JsonResponse(
            {"message": "You must provide the new content for the material"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if "material_id" in request.data:
        return JsonResponse(
            {"message": "You can not change the material id"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        material = Material.objects.get(id=material_id)
        material_html = MaterialHTML.objects.get(material_id=material.id)
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "There is not a material with that id"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except MaterialHTML.DoesNotExist:
        return JsonResponse(
            {"message": "This material does not have HTML content"},
            status=status.HTTP_404_NOT_FOUND,
        )

    for field_name, new_value in request.data.items():
        if hasattr(material_html, field_name):
            setattr(material_html, field_name, new_value)
        else:
            return JsonResponse(
                {"message": f"{field_name} attribute does not exist in material"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    material_html.save()
    serializer = MaterialHTMLSerializer(material_html)

    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@schema(schemas.delete_material_html_schema)
def delete_material_html(request, material_id: int) -> JsonResponse:
    """
    Deletes a material HTML content with its id

    Args:
        request: http request
        material_id (int): material's id to remove its HTML content

    Returns:
        response (JsonResponse): HTTP response in JSON format,
    """

    try:
        material = Material.objects.get(pk=material_id)
        material_html = MaterialHTML.objects.get(material_id=material.id)

        material_html.delete()

        return JsonResponse(
            {"message": "Material deleted successfully"}, status=status.HTTP_200_OK
        )
    except Material.DoesNotExist:
        return JsonResponse(
            {"message": "Material does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    except MaterialHTML.DoesNotExist:
        return JsonResponse(
            {"message": "This material does not have HTML content"},
            status=status.HTTP_404_NOT_FOUND,
        )
