"""Module to create different utilities/functions for the courses app"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from constants.ioc import URL_PROBLEM
import json
import requests
from courses.models import Material
from courses.serializers.material_html_serializer import MaterialHTMLSerializer
from courses.serializers.material_pdf_serializer import MaterialPDFSerializer
from courses.serializers.material_video_serializer import MaterialVideoSerializer
from ioc.serializers.material_io_code_serializer import MaterialIoCodeSerializer
from ioc.serializers.case_serializer import CaseSerializer


def judge(data):
    """Method that creates the problem on the judge files."""

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL_PROBLEM, data=json.dumps(data), headers=headers)
    return response.json(), response.status_code


def creation_case(data):
    """Method that creates the cases on the judge files."""
    for case in range(len(data["input"])):
        case_serializer = CaseSerializer(
            data={
                "input": data["input"][case],
                "output": data["output"][case],
                "id_case": case,
                "material_io_code_id": data["material_io_code_id"],
            }
        )
        if case_serializer.is_valid():
            case_serializer.save()


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
            specific_serializer = MaterialHTMLSerializer(data=validation_data)
        case "VID":
            specific_serializer = MaterialVideoSerializer(data=validation_data)
        case "PDF":
            specific_serializer = MaterialPDFSerializer(data=validation_data)
        case _:
            pass

    validate_for_specific_material_type(specific_serializer, material)
    # -------------------------#
    # validated all necessary checks
    # So we create the specific material
    # -------------------------#

    specific_instance = specific_serializer.save()

    if material_type == "IOC":
        validation_data["problem_id"] = str(material.id)
        judge(validation_data)
        validation_data["material_io_code_id"] = specific_instance.id
        creation_case(validation_data)


def validate_for_specific_material_type(
    material_type_serializer: ModelSerializer | None, material: Material
) -> None:
    if material_type_serializer is not None:
        # A little ugly because is_valid can raise an exception,
        # but given that we need to delete the material if it's not valid,
        # if not done this way, it would mean to override every single
        # is_valid method of each serializers.

        if not material_type_serializer.is_valid():
            # if it's not valid, delete the material already created
            Material.objects.get(id=material.id).delete()
            raise serializers.ValidationError(material_type_serializer.errors)
    else:
        # if it didn't match any case, delete the material already created
        Material.objects.get(id=material.id).delete()
        raise serializers.ValidationError(
            {"material_type": "The material type was not recognized"}
        )
