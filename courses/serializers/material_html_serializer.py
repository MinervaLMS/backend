from rest_framework import serializers

from ..models.material_html import MaterialHTML


class MaterialHTMLSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialHTML
        fields = ["material_id", "content"]

        extra_kwargs = {
            "material_id": {"write_only": True},
        }

    def validate(self, data):
        """
        Verify if material_id is unique,
        verify if material exists and
        verify if material_type is 'HTM'
        """

        material_id = data.get("material_id")

        if MaterialHTML.objects.filter(material_id=material_id).exists():
            raise serializers.ValidationError(
                "This material already has an HTML content"
            )

        if not material_id:
            raise serializers.ValidationError("There is not a material with that id")

        if material_id.material_type != "HTM":
            raise serializers.ValidationError("This material is not type HTML")

        return data

    def create(self, validated_data):
        material = MaterialHTML(**validated_data)
        material.save()

        return material
