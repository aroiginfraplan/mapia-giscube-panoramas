from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Panorama, Project, PointCloud, LocalPointCloud
from .serializers import PanoramaSerializer, ProjectSerializer, PointCloudSerializer, LocalPointCloudSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    lookup_field = 'code'

    @action(detail=True, methods=['get'])
    def panoramas(self, request, code=None):
        latlon = None
        p = request.GET.get('p')
        if p:
            try:
                latlon = p.split(',')
                latlon = list(map(float, latlon))
            except Exception:
                msg = 'ERROR: invalid p parameter'
        else:
            msg = 'ERROR: missing p parameter'
        if not latlon:
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        radius = None
        r = request.GET.get('r')
        if r:
            try:
                radius = int(r)
            except Exception:
                msg = 'ERROR: invalid r parameter'
        else:
            msg = 'ERROR: missing r parameter'
        if not radius:
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        filter = {'project_id': code}
        c = request.GET.get('c')
        if c:
            filter['category'] = c

        sourceid = request.GET.get('sourceid')
        if sourceid is not None:
            filter['sourceid'] = sourceid

        qs = Panorama.objects.filter(**filter)
        geom = Point(latlon[1], latlon[0], srid=4326)
        qs = qs.filter(
            geom__distance_lte=(geom, D(m=radius))
        ).annotate(
            distance=Distance(geom, 'geom')
        ).order_by('distance')
        serializer = PanoramaSerializer(qs, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def point_cloud(self, request, code=None):
        latlon = None
        p = request.GET.get('p')
        if p:
            try:
                latlon = p.split(',')
                latlon = list(map(float, latlon))
            except Exception:
                msg = 'ERROR: invalid p parameter'
        else:
            msg = 'ERROR: missing p parameter'
        if not latlon:
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        filter = {'project_id': code}
        qs = PointCloud.objects.filter(**filter)
        geom = Point(latlon[1], latlon[0], srid=4326)
        qs = qs.filter(
            geom__contains=geom
        )
        serializer = PointCloudSerializer(qs, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def local_point_cloud(self, request, code=None):
        latlon = None
        p = request.GET.get('p')
        if p:
            try:
                latlon = p.split(',')
                latlon = list(map(float, latlon))
            except Exception:
                msg = 'ERROR: invalid p parameter'
        else:
            msg = 'ERROR: missing p parameter'
        if not latlon:
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        filter = {'project_id': code}
        qs = LocalPointCloud.objects.filter(**filter)
        geom = Point(latlon[1], latlon[0], srid=4326)
        qs = qs.filter(
            geom__contains=geom
        )
        serializer = LocalPointCloudSerializer(qs, many=True)

        return Response(serializer.data)
