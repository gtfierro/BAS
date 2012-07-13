import requests
from requests.auth import HTTPBasicAuth
from uuid import UUID
from types import MethodType

class APINode(object):
    def __init__(self, api, name, type, uuid=None, methods=None):
        self.api = api
        self.name = name
        self.type = type
        if uuid is None:
            self.uuid = None
        else:
            self.uuid = UUID(uuid)
        if methods:
            for name in methods:
                self._bind_method(name, methods[name])

    def _bind_method(self, name, doc):
        api = self.api
        def call_method(self, *args, **kwargs):
            return api.call(self,  name, *args, **kwargs)
        call_method.__name__ = str(name)
        call_method.__doc__ = str(doc)
        setattr(self, name, MethodType(call_method, self, APINode))

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'APINode(' + self.name + ', ' + self.type + ', ' + str(self.uuid) + ')'


class APIBuilding(APINode):
    def __init__(self, api, name):
        APINode.__init__(self, api, name, 'Building')

    def __repr__(self):
        return 'APIBuilding(' + self.name + ')'


class APIFloor(APINode):
    def __init__(self, api, name, building):
        APINode.__init__(self, api, name, 'Floor')
        self.building = APIBuilding(api, building)

    def __repr__(self):
        return 'APIFloor(' + self.name + ', ' + self.building + ')'

class APIArea(APINode):
    def __init__(self, api, name, building, floor):
        APINode.__init__(self, api, name, 'Area')
        self.building = APIBuilding(api, building)
        self.floor = APIFloor(api, floor, building)

    def __repr__(self):
        return 'APIArea(' + self.name + ', ' + self.building + ', ' + self.floor + ')'

class AppstackAPI(object):
    def __init__(self, user, password, url='http://localhost:8000'):
        self.url = url + '/webapi'
        self.auth = HTTPBasicAuth(user, password)

    def _format_obj(self, obj):
        if isinstance(obj, list):
            return [self._format_obj(x) for x in obj]
        elif not isinstance(obj, dict):
            return obj
        elif 'type' not in obj or 'name' not in obj:
            return obj
        elif obj['type'] == 'Building':
            return APIBuilding(self, obj['name'])
        elif obj['type'] == 'Floor':
            return APIFloor(self, obj['name'], obj['building'])
        elif obj['type'] == 'Area':
            return APIArea(self, obj['name'], obj['building'], obj['floor'])
        else:
            return APINode(self, obj['name'], obj['type'], obj['uuid'], obj['methods'])

    def _request(self, path):
        r = requests.get(self.url + path, auth=self.auth)
        r.raise_for_status()
        return self._format_obj(r.json)

    def __call__(self, query):
        return self._request('/query?q=' + query)

    def query(self, query):
        return self._request('/query?q=' + query)

    def tag(self, tag):
        return self._request('/tag/' + tag)

    def all(self):
        return self._request('/all')

    def uuid(self, uuid):
        return self._request('/uuid/' + uuid)

    def call(self, obj, method, *args, **kwargs):
        """Call a method on an object or group of objects"""
        if isinstance(obj, list):
            return [self.call(x, method, *args, **kwargs) for x in obj]
        else:
            path = '/uuid/' + str(obj.uuid) + '/' + method + '?'
            if args:
                path += ','.join(str(arg) for arg in args) + '&'
            for k, v in kwargs.items():
                path += str(k) + '=' + str(v) + '&'
            return self._request(path[:-1])
