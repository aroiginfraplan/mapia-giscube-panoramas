from django.conf.urls import include
from django.urls import path

from rest_framework import routers

from .api import ProjectViewSet


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('api/', include(router.urls)),
]
