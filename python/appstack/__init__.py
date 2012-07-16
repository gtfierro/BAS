import requests
from requests.auth import HTTPBasicAuth
from uuid import UUID
from types import MethodType

class Node(object):
    def __init__(self, api, name, type, methods=None):
        self.api = api
        self.name = name
        self.type = type
        if methods:
            for name in methods:
                self._bind_method(name, methods[name])

    def _bind_method(self, name, doc):
        api = self.api
        def call_method(self, *args, **kwargs):
            return api.call(self,  name, *args, **kwargs)
        call_method.__name__ = str(name)
        call_method.__doc__ = str(doc)
        setattr(self, name, MethodType(call_method, self, Node))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Node:{0} {1}>'.format(self.type, self.name)

class Resource(Node):
    def __init__(self, api, name, type, uuid, methods=None):
        Node.__init__(self, api, name, type, methods)
        self.api = api
        self.name = name
        self.type = type
        self.uuid = UUID(uuid)
        if methods:
            for name in methods:
                self._bind_method(name, methods[name])


    def __repr__(self):
        return '<Resource:{0}, {1}, {2}>'.format(self.type, self.name, self.uuid)

class Building(Node):
    def __init__(self, api, name):
        Node.__init__(self, api, name, 'Building')

    def __repr__(self):
        return '<Building {0}>'.format(self.name)


class Floor(Node):
    def __init__(self, api, name, building):
        Node.__init__(self, api, name, 'Floor')
        self.building = Building(api, building)

    def __repr__(self):
        return '<Floor {0}:{1}>'.format(self.building, self.name)

class Area(Node):
    def __init__(self, api, name, building, floor):
        Node.__init__(self, api, name, 'Area')
        self.building = Building(api, building)
        self.floor = Floor(api, floor, building)

    def __repr__(self):
        return '<Area {0}:{1}:{2}>'.format(self.building, self.floor, self.name)

class Appstack(object):
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
            return Building(self, obj['name'])
        elif obj['type'] == 'Floor':
            return Floor(self, obj['name'], obj['building'])
        elif obj['type'] == 'Area':
            return Area(self, obj['name'], obj['building'], obj['floor'])
        else:
            return Resource(self, obj['name'], obj['type'], obj['uuid'], obj['methods'])

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
