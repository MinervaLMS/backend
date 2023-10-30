"""Module to create different utilities/functions for the courses app"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from constants.ioc import URL_PROBLEM
import json
import requests
from constants.ioc import LIST_IOC
from courses.models import Material
from courses.serializers.material_html_serializer import MaterialHTMLSerializer
from courses.serializers.material_video_serializer import MaterialVideoSerializer
from ioc.serializers.material_io_code_serializer import MaterialIoCodeSerializer
from ioc.serializers.case_serializer import CaseSerializer


def judge(data):
    """Method that creates the problem on the judge files."""

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL_PROBLEM, data=json.dumps(data), headers=headers)
    return response.json(), response.status_code


def material_ioc_validate(data):
    """Method that validates if the ioc material has all the required fields"""
    missing = [element for element in LIST_IOC if element not in data]
    return missing


# ------Methods for material creation in their specific tables------


def create_ioc_material(data, material):
    """Method that creates the ioc material on the judge files
    and the cases associated with it."""

    data["material_id"] = material
    serializer = MaterialIoCodeSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        data["problem_id"] = data["name"]
        judge(data)
        for case in range(len(data["input"])):
            serializer_case = CaseSerializer(
                data={
                    "id_case": case,
                    "input": data["input"][case],
                    "output": data["output"][case],
                    "material_io_code_id": serializer.data["id"],
                }
            )

            if serializer_case.is_valid():
                serializer_case.save()
            # TODO: What happens if this is not valid?


def create_htm_material(data, material_id):
    """Method that creates the htm material on the material html database table"""
    from rest_framework import serializers

    print("Should've raise validation error, m8.")
    raise serializers.ValidationError("Raised validation error for html material.")


def create_vid_material(data):
    """Method that creates the vid material on the material video database table"""
    pass


def validate_and_create_specific_material_type(
    validation_data: dict, material: Material
) -> None:
    """
    Method that checks the specific material type and validates the
    material for that specific type if it is valid,
    it creates the material in the specific material table.
    """

    material_type = validation_data.get("material_type")
    validation_data["material_id"] = material.id
    specific_serializer: ModelSerializer | None = None

    # match statement is supposed to be faster than if-else
    match material_type:
        case "IOC":
            specific_serializer = MaterialIoCodeSerializer(data=validation_data)
        case "HTM":
            # validation_data["content"] = "MY HTML"
            specific_serializer = MaterialHTMLSerializer(data=validation_data)
        case "VID":
            validation_data[
                "external_id"
            ] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
            specific_serializer = MaterialVideoSerializer(data=validation_data)
        case "PDF":
            # validation_data["content"] = "PDF"
            specific_serializer = MaterialHTMLSerializer(data=validation_data)
        case _:
            pass

    validate_for_specific_material_type(specific_serializer, material)
    # -------------------------#
    # validated all necessary checks
    # So we create the specific material
    # -------------------------#

    specific_serializer.save()


def validate_for_specific_material_type(
    material_type_serializer: ModelSerializer | None, material: Material
) -> None:
    if material_type_serializer is not None:
        # A little ugly because is_valid can raise an exception,
        # but given that we need to delete the material if it's not valid,
        # if not done this way, it would mean to override every single
        # is_valid method of each serializers.

        if not material_type_serializer.is_valid():
            Material.objects.get(id=material.id).delete()
            raise serializers.ValidationError(material_type_serializer.errors)
    else:
        # if it didn't match any case, delete the material already created
        Material.objects.get(id=material.id).delete()
