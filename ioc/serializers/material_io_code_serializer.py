from rest_framework import serializers

from ..models.material_io_code import MaterialIoCode


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
        return data

    def create(self, validated_data):
        material_io_code = MaterialIoCode(**validated_data)
        material_io_code.save()

        return material_io_code


class MaterialGetIoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialIoCode
        fields = "__all__"
