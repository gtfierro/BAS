import sys, os
sys.path.append(os.path.abspath('./geo'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from smapgeo.models import *

class BuildingsList(object):
    """
    The purpose of this class is to provide a dictionary-like interface to the list of
    all of the buildings in the database.

    Usage:
      gis.buildings['Sutardja Dai Hall']

      for b in gis.buildings:
        foo(b)
    """
    def __getitem__(self, key):
        try:
            return Building.objects.get(name=key)
        except:
            raise KeyError("Building not found")

    def __setitem__(self, key, value):
        assert False

    def __iter__(self):
        for b in Building.objects.all():
            yield b

buildings=BuildingsList()
