from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import json

import os, sys
APPSTACK_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
sys.path.append(APPSTACK_PATH)

import lexerparser
import node_types

class JSONResponse(HttpResponse):
    def __init__(self, d):
        HttpResponse.__init__(self, json.dumps(d), mimetype='application/json')

    @staticmethod
    def encode_obj(obj):
        if isinstance(obj, lexerparser.gis.Area):
            return {
            'name': obj.name,
            'type': 'Area',
            'floor': obj.floor.name,
            'building': obj.floor.building.name,
            }
        elif isinstance(obj, lexerparser.gis.Floor):
            return {
            'name': obj.name,
            'type': 'Floor',
            'building': obj.building.name,
            }
        elif isinstance(obj, lexerparser.gis.Building):
            return {
            'name': obj.name,
            'type': 'Building'
            }
        else:
            return {
                'name': obj.name,
                'type': obj.type(),
                'uuid': str(obj.uid),
                'methods': node_types.get_methods(obj)
                }

    @staticmethod
    def encode_objs(objs):
        return [JSONResponse.encode_obj(obj) for obj in objs]

    @staticmethod
    def error(s):
        return HttpResponseBadRequest(json.dumps(s), mimetype="application/json")

class HTMLResponse(HttpResponse):
    def __init__(self, s):
        HttpResponse.__init__(self, s)

    @staticmethod
    def encode_obj(obj):
        return loader.get_template('obj.html').render(Context({
                'url_prefix' : '/webapi/',
                'obj' : JSONResponse.encode_obj(obj)
                }))
    @staticmethod
    def encode_objs(objs):
        return loader.get_template('objs.html').render(Context({
                'url_prefix' : '/webapi/',
                'objs' : JSONResponse.encode_objs(objs)
                }))
    @staticmethod
    def error(s):
        return HttpResponseBadRequest(s)


class Response(object):
    @staticmethod
    def get_class(output):
        if output == 'json':
            return JSONResponse
        elif output == 'html':
            return HTMLResponse
        else:
            assert False, 'Invalid output type'

    @staticmethod
    def obj(output, obj):
        cls = Response.get_class(output)
        if isinstance(obj, list):
            if not obj:
                return cls.error('Invalid object')
            else:
                obj = obj[0]
        return cls(cls.encode_obj(obj))

    @staticmethod
    def objs(output, objs):
        cls = Response.get_class(output)
        return cls(cls.encode_objs(objs))

    @staticmethod
    def error(output, s):
        cls = Response.get_class(output)
        return cls.error(s)

    @staticmethod
    def text(output, s):
        cls = Response.get_class(output)
        return cls(s)


def index(request):
    t = loader.get_template('index.html')
    c = Context({
        'url_prefix' : '/webapi/',
        'geo_prefix' : '/smapgeo/'
        })
    return HttpResponse(t.render(c))

def t(request, tag, output='json'):
    q = lexerparser.query('.' + tag)
    return Response.objs(output, q)

def all_objs(request, output='json'):
    q = lexerparser.query('.')
    return Response.objs(output, q)


def uuid(request, uuid, output='json'):
    q = lexerparser.query('^' + uuid)
    return Response.obj(output, q)

def uuid_method(request, uuid, method, output='json'):
    q = lexerparser.query('^' + uuid)
    if not q:
        Response.error(output, 'Invalid object')
    return call_method(request, q[0], method)

def call_method(request, obj, method, output='json'):
    if not method in node_types.get_methods(obj):
        return Response.error(output, 'Invalid method for object')
    if not request.GET:
        args = ()
        kwargs = {}
    elif len(request.GET) == 1 and request.GET.values()[0] == '':
        args = (json.loads(request.GET.keys()[0]), )
        kwargs = {}
    else:
        args = ()
        kwargs = {}
        for key in request.GET:
            kwargs[key] = json.loads(request.GET[key])
    res = getattr(obj, method)(*args, **kwargs)
    return Response.text(output, res)

def query(request, output='json'):
    if 'q' not in request.GET:
        return Response.error(output, "No query string given")
    string = request.GET['q']
    q = lexerparser.query(string.replace('+', ' '))
    if q is None:
        return Response.error(output, "Error processing query")
    return Response.objs(output, q)

def geo(request):
    t = loader.get_template('geo.html')
    if 'building' not in request.GET:
        return Response.objs('html', list(lexerparser.gis.buildings))
    building_name = request.GET['building']
    if building_name not in lexerparser.gis.buildings:
        return Response.error('html', "Could not find building")
    building = lexerparser.gis.buildings[building_name]
    c = Context({
        'heading' : 'Buildings',
        'url_prefix' : '/webapi/',
        'geo_prefix' : '/smapgeo/',
        'building' : building
        })
    return HttpResponse(t.render(c))
