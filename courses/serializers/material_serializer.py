from rest_framework import serializers
from ..models.material import Material
from courses.utils import (
    material_ioc_validate,
    validate_and_create_specific_material_type,
)
from courses.utils import create_ioc_material


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
                {"order": "This order in this module is already in use"}
            )

        if data.get("material_type") != data.get("material_type").upper():
            raise serializers.ValidationError(
                {"material_type": "The material type must be in uppercase."}
            )

        if data.get("material_type") == "IOC":
            result_ioc = material_ioc_validate(self.initial_data)
            if result_ioc:
                raise serializers.ValidationError(
                    {"material_type": f"The value {result_ioc[0]} is missing."}
                )
            if self.initial_data["max_memory"] < 300:
                raise serializers.ValidationError(
                    {"max_memory": "The value max_memory must be greater than 300."}
                )

        return data

    def create(self, validated_data):
        """When a material is created, if it is an ioc,
        it is also created in the ioc table."""

        material = Material(**validated_data)
        material.save()

        validate_and_create_specific_material_type(self.initial_data, material)

        if validated_data.get("material_type") == "IOC":
            create_ioc_material(self.initial_data, material.id)

        return material
