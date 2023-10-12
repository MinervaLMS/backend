from rest_framework import serializers

from ..models.material import Material

from ioc.serializers.material_io_code_serializer import MaterialIoCodeSerializer


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

        data_ioc = self.initial_data
        material_id = material.id

        if validated_data.get("material_type") == "ioc":
            data_ioc["material_id"] = material_id
            serializer = MaterialIoCodeSerializer(data=data_ioc)
            if serializer.is_valid():
                serializer.save()

        return material
