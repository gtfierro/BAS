"""Portions of this code are borrowed from Django fixture magic"""
import sys
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from models import Building
from django.db import models
from django.core.serializers import serialize
from django.template import Variable, VariableDoesNotExist

def get_fields(obj):
    try:
        return obj._meta.fields
    except AttributeError:
        return []


class GeoSerializer(object):
    def __init__(self):
        self.serialize_me = []
        self.seen = {}

    def add(self, building, floor=None, area=None):
        b = Building.objects.filter(name=building)[0]
        if floor is not None:
            f = b[floor]
            if area is not None:
                a = f[area]
                self.add_to_serialize_list([a])
                return
            self.add_to_serialize_list([f])
            self.add_to_serialize_list(f.areas.all())
            self.add_to_serialize_list(f.views.all())
            return

        self.add_to_serialize_list([b])
        for f in b.floors.all():
            self.add_to_serialize_list([f])
            self.add_to_serialize_list(f.areas.all())
            self.add_to_serialize_list(f.views.all())

    def serialize_fully(self):
        index = 0

        while index < len(self.serialize_me):
            for field in get_fields(self.serialize_me[index]):
                if isinstance(field, models.ForeignKey):
                    self.add_to_serialize_list(
                        [self.serialize_me[index].__getattribute__(field.name)])

            index = index + 1

        self.serialize_me.reverse()

        data = serialize('json', [o for o in self.serialize_me if o is not None],
                         indent=4)
        return data

    def add_to_serialize_list(self, objs):
        for obj in objs:
            if obj is None:
                continue
            if not hasattr(obj, '_meta'):
                self.add_to_serialize_list(obj)
                continue

            # Proxy models don't serialize well in Django.
            if obj._meta.proxy:
                obj = obj._meta.proxy_for_model.objects.get(pk=obj.pk)

            key = "%s:%s:%s" % (obj._meta.app_label, obj._meta.module_name,
                                obj.pk)
            if key not in self.seen:
                self.serialize_me.append(obj)
                self.seen[key] = 1
