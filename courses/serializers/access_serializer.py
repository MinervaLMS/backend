from rest_framework import serializers

from ..models.access import Access


class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Access
        fields = "__all__"

    def validate(self, data):
        """Verify if unique tuple material_id and user_id is duplicated

        Args:
            data (dict): Access data
        """
        user_id: int = data.get("user_id")
        material_id: int = data.get("material_id")

        if Access.objects.filter(user_id=user_id, material_id=material_id).exists():
            raise serializers.ValidationError(
                "This user has already accessed to this material"
            )

        return data
