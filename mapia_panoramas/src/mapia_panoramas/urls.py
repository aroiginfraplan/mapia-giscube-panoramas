from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from .api import ProjectViewSet
from .views import serve_panoramas_files


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('api/', include(router.urls)),
    path('files/<code>/<path:path>', serve_panoramas_files, name='panoramas-files'),
]
