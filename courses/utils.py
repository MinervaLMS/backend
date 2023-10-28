"""Module to create different utilities/functions for the courses app"""
from constants.ioc import URL_PROBLEM
import json
import requests
from constants.ioc import LIST_IOC
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


def material_ioc_create(data, material):
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
