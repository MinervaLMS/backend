from rest_framework import serializers

from courses.models.module_progress import Module_progress


class ModuleProgressSerializer(serializers.ModelSerializer):
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
        if Module_progress.objects.filter(
            user_id=user_id, module_id=module_id
        ).exists():
            raise serializers.ValidationError(
                "This user in this module is already in use"
            )
        return data

    def create(self, validated_data):
        module_progress = Module_progress(**validated_data)
        module_progress.save()

        return module_progress


class GetModuleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module_progress
        exclude = ("id", "user_id")
