from rest_framework import serializers

from .models import Panorama, Project


class PanoramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panorama
        fields = ('id', 'project', 'category', 'filename', 'filetype', 'sourceid', 'capture', 'altitude', 'roll',
                  'pitch', 'pan', 'geom')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('code', 'name')
