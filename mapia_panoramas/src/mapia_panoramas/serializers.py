from rest_framework import serializers

from .models import Panorama, Project


class PanoramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panorama
        fields = ('id', 'projecte', 'filename', 'filetype', 'sourceid',
                  'timestamp', 'geom', 'altitude', 'roll', 'pitch', 'pan')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('code', 'name')
