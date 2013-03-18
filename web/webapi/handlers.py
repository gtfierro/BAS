from piston.handler import BaseHandler
from piston.utils import rc, throttle
import json
import ast
import sys
from StringIO import StringIO

from appstack import lexerparser, node_types

class TagHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, tag):
        q = lexerparser.query('.' + tag)
        return q

class QueryHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        if 'q' not in request.GET:
            return rc.BAD_REQUEST
        string = request.GET['q']
        q = lexerparser.query(string.replace('+', ' '))
        if q is None:
            return rc.BAD_REQUEST

        return q

class AllHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        q = lexerparser.query('.')
        return q

class UUIDHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, uuid):
        q = lexerparser.query('^' + uuid)
        return q[0] if q else rc.NOT_FOUND

class UUIDMethodHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, uuid, method):
        q = lexerparser.query('^' + uuid)
        if not q:
            return rc.NOT_FOUND

        obj = q[0]
        if not method in node_types.get_methods(obj):
            return rc.BAD_REQUEST
        if not request.GET:
            args = ()
            kwargs = {}
        elif len(request.GET) == 1 and request.GET.values()[0] == '':
            args = [json.loads(x) for x in request.GET.keys()[0].split(',')]
            kwargs = {}
        else:
            args = ()
            kwargs = {}
            for key in request.GET:
                kwargs[key] = json.loads(request.GET[key])
        res = getattr(obj, method)(*args, **kwargs)
        return res

class CodeHandler(BaseHandler):
    methods_allowed = ('POST',)

    def create(self, request):
        """
        [domain] is the list of objects referenced by the 'bas' variable
        [code] is the code we want to run on those objects
        """
        if request.data:
            data = request.data
            domain = ast.literal_eval(data['domain'])
            objs = [lexerparser.get_uuid(x) for x in domain]
            l = locals()
            l['bas'] = objs
            code = compile(data['code'],'<string>','exec')
            output = StringIO()
            sys.stdout = output
            sys.stderr = output
            eval(code, l)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            val = output.getvalue()
            print val
            return val
