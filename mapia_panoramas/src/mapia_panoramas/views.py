import mimetypes
import os
import stat

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since

import boto3
from botocore.client import Config

from .settings import (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME, AWS_S3_ENDPOINT_URL,
                       AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, PANORAMAS_ROOT, PANORAMAS_PUBLIC)


def panoramas_files_server(request, code, path):
    if not PANORAMAS_PUBLIC and not request.user.is_authenticated:
        raise PermissionDenied

    path = os.path.join(code, path)
    fullpath = os.path.realpath(os.path.join(PANORAMAS_ROOT, path))
    panoramas_full_path = os.path.realpath(os.path.join(PANORAMAS_ROOT, code))

    if not os.path.exists(fullpath) or not fullpath.startswith(panoramas_full_path):
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

    http_range = request.META.get('HTTP_RANGE')
    if http_range:
        response = files_by_range(http_range, fullpath, content_type)
    else:
        response = HttpResponse(
            open(fullpath, 'rb').read(),
            content_type=content_type
        )
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


def files_by_range(http_range, fullpath, content_type):
    if not (http_range and http_range.startswith('bytes=') and http_range.count('-') == 1):
        return HttpResponse()

    f = open(fullpath, 'rb')
    statobj = os.fstat(f.fileno())
    start, end = http_range.split('=')[1].split('-')
    if not start:  # requesting the last N bytes
        start = max(0, statobj.st_size - int(end))
        end = ''
    start, end = int(start or 0), int(end or statobj.st_size - 1)
    assert 0 <= start < statobj.st_size, (start, statobj.st_size)
    end = min(end, statobj.st_size - 1)
    f.seek(start)
    old_read = f.read
    f.read = lambda n: old_read(min(n, end + 1 - f.tell()))
    response = HttpResponse(
        f.read(end),
        content_type=content_type
    )
    response.status_code = 206
    response['Content-Length'] = end + 1 - start
    response['Content-Range'] = 'bytes %d-%d/%d' % (start, end, statobj.st_size)
    return response
