from rest_framework import serializers

from ..models.material import Material

from ioc.serializers.material_io_code_serializer import MaterialIoCodeSerializer

from constants.ioc import URL_PROBLEM
import json
import requests


def judge(data):
    """Method that creates the problem on the judge files."""

    headers = {"Content-Type": "application/json"}
    response = requests.post(URL_PROBLEM, data=json.dumps(data), headers=headers)
    return response.json(), response.status_code


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"

    def validate(self, data):
        """
        Verify if unique tuple module_id and order is duplicated.
        """

        module_id = data.get("module_id")
        order = data.get("order")

        if Material.objects.filter(module_id=module_id, order=order).exists():
            raise serializers.ValidationError(
                "This order in this module is already in use"
            )

        return data

    def create(self, validated_data):
        """When a material is created, if it is an ioc,
        it is also created in the ioc table."""

        material = Material(**validated_data)
        material.save()

        if validated_data.get("material_type") == "ioc":
            data_ioc = self.initial_data
            material_id = material.id
            data_ioc["material_id"] = material_id
            serializer = MaterialIoCodeSerializer(data=data_ioc)

            if serializer.is_valid():
                data_ioc["problem_id"] = data_ioc["name"]
                judge(data_ioc)
                serializer.save()

        return material
