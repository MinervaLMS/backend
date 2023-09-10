from rest_framework import serializers

from courses.models.module_progress import Module_progress
from courses.models.module import Module
from accounts.models.user import User


class Module_progressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module_progress
        fields = "__all__"

    def validate(self, data):
        """
        Verify if unique tuple user_id and module_id is duplicated,
        Verify user_id and module_id, verify if user and module exists.
        """

        user_id = data.get("user_id")
        module_id = data.get("module_id")

        if Module_progress.objects.filter(user_id=user_id, module_id=module_id).exists():
            raise serializers.ValidationError(
                "This user in this module is already in use"
            )

        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("This user does not exist")

        if not Module.objects.filter(id=module_id).exists():
            raise serializers.ValidationError("This module does not exist")

        return data

    def create(self, validated_data):
        module_progress = Module_progress(**validated_data)
        module_progress.save()

        return module_progress
