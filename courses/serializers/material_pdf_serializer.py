from rest_framework import serializers

from ..models.material_pdf import MaterialPDF


class MaterialPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialPDF
        fields = ("material_id", "url", "pages")

    def validate(self, data):
        """
        Verify if material_id is unique,
        verify if material exists and
        verify if material_type is 'PDF'
        """

        material_id = data.get("material_id")

        if MaterialPDF.objects.filter(material_id=material_id).exists():
            raise serializers.ValidationError(
                "This material already has an PDF content"
            )

        if not material_id:
            raise serializers.ValidationError("There is not a material with that id")

        if material_id.material_type != "PDF":
            raise serializers.ValidationError("This material is not type PDF")

        return data

    def create(self, validated_data):
        material_pdf = MaterialPDF(**validated_data)
        material_pdf.save()
        return material_pdf
