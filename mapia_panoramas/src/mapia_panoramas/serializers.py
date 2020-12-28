from rest_framework import serializers

from .models import Lateral, Panorama, Project, PointCloud

class LateralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lateral
        fields = ('file_name', 'file_type', 'file_folder', 'pan')

class PanoramaSerializer(serializers.ModelSerializer):
    laterals = LateralSerializer(many=True, read_only=True)

    class Meta:
        model = Panorama
        fields = ('id', 'project', 'category', 'file_name', 'file_type', 'file_folder', 'source_id', 'date', 'altitude',
                  'roll', 'pitch', 'pan', 'geom', 'laterals')

class PointCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointCloud
        fields = ('id', 'project', 'code', 'name', 'file_folder', 'geom')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('code', 'name', 'description', 'zone', 'date_start', 'date_end',
                  'folder_panorama', 'folder_images', 'folder_point_cloud', 'layer_panorama')
