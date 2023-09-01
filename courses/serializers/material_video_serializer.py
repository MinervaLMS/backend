from rest_framework import serializers

from ..models.material_video import MaterialVideo
from pytube import YouTube


class MaterialVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        fields = ["external_id", "material_id"]

    def validate(self, data):
        """
        Verify if unique material_id is duplicated.
        """

        material_id = data.get("material_id")

        if MaterialVideo.objects.filter(material_id=material_id).exists():
            raise serializers.ValidationError("This material_id is already in use")

        if not self.validate_youtube_link(data.get("external_id")):
            raise serializers.ValidationError(
                "The external_id should be a valid YouTube link"
            )

        return data

    def validate_youtube_link(self, link):
        try:
            YouTube(link)
            return True
        except Exception:
            return False

    def get_video_length(self, url):
        try:
            video = YouTube(url)
            length = video.length
            return length
        except Exception as e:
            return str(e)

    def create(self, validated_data):
        # Youtube is the only video service that we considered
        material_video = MaterialVideo(**validated_data)
        external_id = validated_data.get("external_id")

        length = self.get_video_length(external_id)
        material_video.length = int(length)

        material_video.source = "y"
        material_video.save()

        return material_video


class MaterialGetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        fields = "__all__"
