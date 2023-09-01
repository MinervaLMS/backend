from rest_framework import serializers

from ..models import MaterialVideo
from pytube import YouTube

class MaterialVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        fields = ["external_id", "material_id"]

    def validate(self, data):
        """
        Verify if unique material_id is duplicated.
        """

        material_id = data.get('material_id')

        if MaterialVideo.objects.filter(material_id=material_id).exists():
            raise serializers.ValidationError(
                "This material_id is already in use")
        
        if not self.validlink(data.get('external_id')):
            raise serializers.ValidationError(
                "The external_id should be a valid YouTube link")

        return data
    
    def validlink(self, enlace):
        try:
            video = YouTube(enlace)
            return True
        except Exception:
            return False
        
    def video_length(self, url):
        try:
            video = YouTube(url)
            length = video.length
            return length
        except Exception as e:
            return str(e)
        
    def create(self, validated_data):
        materialVideo = MaterialVideo(**validated_data)
        external_id = validated_data.get('external_id')
        print("CFDD")
        length = self.video_length(external_id)
        print("abc")
        materialVideo.length = int(length)
        materialVideo.source= 'y' #youtube is the only video service that we considered
        print(materialVideo)
        materialVideo.save()

        return materialVideo
    
class MaterialGetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        fields = "__all__"