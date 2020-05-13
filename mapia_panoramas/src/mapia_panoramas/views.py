import mimetypes
import os
import stat

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import Http404, HttpResponseNotModified
from django.utils.decorators import method_decorator
from django.utils.http import http_date
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.static import was_modified_since

from oauth2_provider.decorators import protected_resource


from .settings import PANORAMAS_ROOT


xframe_options_exempt_m = method_decorator(xframe_options_exempt, name='dispatch')


@protected_resource()
@xframe_options_exempt_m
def panoramas_files_server(request, code, path):
    if not request.user.is_authenticated:
        raise PermissionDenied

    path = os.path.join(code, path)
    fullpath = os.path.join(PANORAMAS_ROOT, path)
    if not os.path.exists(fullpath) or \
            not os.path.realpath(fullpath).startswith(os.path.join(PANORAMAS_ROOT, code)):
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
