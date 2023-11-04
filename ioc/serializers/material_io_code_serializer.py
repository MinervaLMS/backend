from rest_framework import serializers

from ..models.material_io_code import MaterialIoCode
from ioc.serializers.utils import material_ioc_validate


class MaterialIoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialIoCode
        fields = "__all__"

    def validate(self, data):
        """
        Verify if unique material_id is duplicated.
        """

        material_id = data.get("material_id")
        if MaterialIoCode.objects.filter(material_id=material_id).exists():
            raise serializers.ValidationError("This material_id is already in use")

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
        material_io_code = MaterialIoCode(**validated_data)
        material_io_code.save()

        return material_io_code


class MaterialGetIoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialIoCode
        fields = "__all__"
