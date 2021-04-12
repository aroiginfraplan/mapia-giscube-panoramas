import mimetypes
import os
import stat

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since

import boto3
from botocore.client import Config
from oauth2_provider.decorators import protected_resource

from .settings import (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME, AWS_S3_ENDPOINT_URL,
                       AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, PANORAMAS_ROOT)


@protected_resource()
def panoramas_files_server(request, code, path):
    if not request.user.is_authenticated:
        raise PermissionDenied

    path = os.path.join(code, path)
    fullpath = os.path.join(PANORAMAS_ROOT, path)
    if not os.path.exists(fullpath) or not os.path.realpath(fullpath).startswith(os.path.join(PANORAMAS_ROOT, code)):
        if AWS_STORAGE_BUCKET_NAME:
            return panoramas_files_s3(request, path)
        else:
            raise Http404('"{0}" does not exist'.format(path))
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    content_type = mimetypes.guess_type(
        fullpath)[0] or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified(content_type=content_type)
    response = HttpResponse(
        open(fullpath, 'rb').read(), content_type=content_type)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    # filename = os.path.basename(path)
    # response['Content-Disposition'] = smart_str(u'attachment; filename={0}'.format(filename))
    return response


def panoramas_files_s3(request, path):
    s3 = boto3.client(
        service_name='s3',
        region_name=AWS_S3_REGION_NAME,
        endpoint_url=AWS_S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'addressing_style': 'virtual'})
    )
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        ExpiresIn=3600,
        Params={
            "Bucket": AWS_STORAGE_BUCKET_NAME,
            "Key": path,
        },
    )
    return HttpResponseRedirect(url)
