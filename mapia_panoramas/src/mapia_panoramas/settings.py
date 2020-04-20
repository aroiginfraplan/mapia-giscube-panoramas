import os
from django.conf import settings

PANORAMAS_ROOT = os.environ.get(
    'PANORAMAS_ROOT', os.path.join(settings.MEDIA_ROOT, 'panoramas')).rstrip('/')
