import os

from email.base64mime import body_encode
from io import BytesIO
from typing import Union
from zipfile import ZipFile

import yaml
from dict2xml import dict2xml
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from lxml import etree
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import YamlLexer
from pygments.lexers.html import XmlLexer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseNotAllowed
from django.http import Http404


@require_http_methods(["GET"])
def show_environment_variables(req: WSGIRequest, format: str = 'html', filename: str = 'data.zip') -> Union[JsonResponse, HttpResponse]:
    """The main entry method returns all environment variables using the format as format type. Example JSON returns JSON response.
        Default value is JSON

    Todo:
        * Create key for ws on settings
        * Use setting.DEBUG to enable this WS
        *

    Args:
        req (WSGIRequest): [description]
        format (str): [description]

    Returns:
        Union[JsonResponse,HttpResponse]: [description]
    """
    d = dict(sorted(os.environ.items()))

    format = format.lower()
    print(format)

    if filename.find('.') == -1:
        filename += '.zip'

    if format == 'json':
        return JsonResponse(d, safe=False)
    elif format == 'xml':
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(dict2xml(d, wrap='root'), parser=parser)
        return HttpResponse(etree.tostring(root), content_type='application/xhtml+xml', status=200)
    elif format == 'txt':
        return HttpResponse(str(d), content_type='text/txt; charset=utf-8', status=200)
    elif format == 'yaml' or format == 'yml':
        return HttpResponse(yaml.dump(d, sort_keys=False, indent=4), content_type='text/yaml', status=200)
    elif format == 'pretty' or format == 'ymlc':
        return HttpResponse(highlight(yaml.dump(d, sort_keys=False, indent=2), YamlLexer(), HtmlFormatter(full=True)), content_type='text/html', status=200)
    elif format == 'prettyxml':
        return HttpResponse(highlight(dict2xml(d, wrap='root', indent='    '), XmlLexer(), HtmlFormatter(full=True)), content_type='text/html', status=200)
    elif format == 'base64' or format == '64':
        return HttpResponse(body_encode(str(d).encode('utf-8')), content_type='text/text; charset=utf-8', status=200)
    elif format == 'html':
        return render(req, "mainws/index.html")

    elif format == 'zip':
        in_memory = BytesIO()
        zf = ZipFile(in_memory, mode="w")
        zf.writestr('data.txt', str(d))
        zf.close()
        in_memory.seek(0)
        return HttpResponse(in_memory.read(), content_type='application/octet-stream', headers={f'Content-Disposition': f'attachment; filename="{filename}"'}, status=200)
    else:
        return HttpResponse(status=404)



def validate_params(req:WSGIRequest)->json:
    if len(req.body) == 0:
                raise NullFormException('dictionary not present on request')

    return json()



@csrf_exempt
def update_environment_variables(req: WSGIRequest) -> Union[JsonResponse, HttpResponse, HttpResponseNotAllowed]:

    r = req.method
    if r == "GET":
        raise Http404("NOT FOUND")

    elif r == "DELETE":
        validate_params(req)
        return JsonResponse({'greg': req.method})

    elif r == "PUT":
        return JsonResponse({'greg': req.method})

    elif r == "POST":
        return JsonResponse({'greg': req.method})

    else:
        return HttpResponseNotAllowed(['DELETE', 'POST', 'PUT'])
