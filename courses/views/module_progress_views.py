from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.module import Module
from ..models.module_progress import Module_progress
from ..serializers.module_progress_serializer import Module_progressSerializer
from ..schemas import module_progress as schemas


@api_view(["POST"])
@schema(schemas.create_module_progress_schema)
@permission_classes([IsAuthenticated])
def create_module_progress(request) -> JsonResponse:
    """
    View to create a new module_progress from a module and user in the database

    Args:
        request: request http with module_progress data
            user_id
            module_id

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """

    serializer = Module_progressSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {"message": "Module_progress created successfully"},
            status=status.HTTP_201_CREATED,
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@schema(schemas.get_module_progress_schema)
@permission_classes([IsAuthenticated])
def get_module_progress(request, user_id: int, module_id: int) -> JsonResponse:
    """
    Get module_progress by its id

    Args:
        request: request http
        user_id (int): user's id to get it
        module_id (int): module's id to get it
    Returns:
        Json response with the fields of the serialized
        module_progress if the user making the request is
        Authenticated, else throws 401 Unauthorized
        status or 404 if module_progress does not exist
    """
    try:
        module_progress = Module_progress.objects.get(
            user_id=user_id, module_id=module_id)
    except Module_progress.DoesNotExist:
        return JsonResponse({"message": "Module_progress not found"}, status=status.HTTP_404_NOT_FOUND)
    module = Module.objects.get(id=module_id)
    if module.module_instructional_materials < module_progress.module_instructional_progress:
        module_progress.module_instructional_progress = module.module_instructional_materials
    if module.module_assessment_materials < module_progress.module_assessment_progress:
        module_progress.module_assessment_progress = module.module_assessment_materials
    serializer = Module_progressSerializer(module_progress)
    data = serializer.data.copy()
    data["module_instructional_progress"] = round(
        data["module_instructional_progress"]/module.module_instructional_materials, 2)*100 if module.module_instructional_materials != 0 else 0
    data["module_assessment_progress"] = round(
        data["module_assessment_progress"]/module.module_assessment_materials, 2)*100 if module.module_assessment_materials != 0 else 0
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@schema(schemas.get_all_modules_progress_schema)
@permission_classes([IsAuthenticated])
def get_all_module_progress(request, user_id: int) -> JsonResponse:
    """
    Get all module_progress by its id

    Args:
        request: request http
        user_id (int): user's id to get it
    Returns:
        Json response with the fields of the serialized
        module_progress if the user making the request is
        Authenticated, else throws 401 Unauthorized
        status or 404 if module_progress does not exist
    """
    try:
        module_progress = Module_progress.objects.filter(user_id=user_id)
    except Module_progress.DoesNotExist:
        return JsonResponse({"message": "Module_progress not found"}, status=status.HTTP_404_NOT_FOUND)
    list_progress: list = []
    for progress in module_progress:
        module: Module = progress.module_id
        data: dict = {
            "module_id": module.id,
            "module_name": module.name,
            "module_instructional_progress": round(
                progress.module_instructional_progress/module.module_instructional_materials, 2)*100 if module.module_instructional_materials != 0 else 0,
            "module_assessment_progress": round(
                progress.module_assessment_progress/module.module_assessment_materials, 2)*100 if module.module_assessment_materials != 0 else 0
        }
        list_progress.append(data)
    return JsonResponse(list_progress, safe=False, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@schema(schemas.update_module_progress_schema)
@permission_classes([IsAuthenticated])
def update_module_progress(request, user_id: int, module_id: int) -> JsonResponse:
    """
    View to update a module_progress from a module and user in the database

    Args:
        request: request http with module_progress data
            user_id (int): user's id to update it
            module_id (int): module's id to update it
            material_type: instrucional or assessment
            type (bool): True: add, False: remove

    Returns:
        response (JsonResponse): HTTP response in JSON format
    """
    if "material_type" not in request.data or "type" not in request.data:
        return JsonResponse({"message": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        module_progress = Module_progress.objects.get(
            user_id=user_id, module_id=module_id)
    except Module_progress.DoesNotExist:
        return JsonResponse({"message": "Module_progress not found"}, status=status.HTTP_404_NOT_FOUND)
    module = Module.objects.get(id=module_id)
    sum: int = 0
    if request.data.get("type") == True:
        sum = 1
    elif request.data.get("type") == False:
        sum = -1
    else:
        return JsonResponse({"message": "Type incorrect"}, status=400)
    if request.data.get("material_type") == "instructional":
        module_progress.module_instructional_progress += sum
        if module_progress.module_instructional_progress >= module.module_instructional_materials:
            module_progress.module_instructional_progress = module.module_instructional_materials
        elif module_progress.module_instructional_progress < 0:
            module_progress.module_instructional_progress = 0
    elif request.data.get("material_type") == "assessment":
        module_progress.module_assessment_progress += sum
        if module_progress.module_assessment_progress >= module.module_assessment_materials:
            module_progress.module_assessment_progress = module.module_assessment_materials
        elif module_progress.module_assessment_progress < 0:
            module_progress.module_assessment_progress = 0
    else:
        return JsonResponse({"message": "Material type incorrect"}, status=400)
    module_progress.save()
    return JsonResponse({"message": "Module_progress modified successfully"}, safe=False, status=status.HTTP_200_OK)
