import sys, os
from collections import deque
sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from smapgeo.models import *
from smapgeo import serialization
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import fromstr

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

    def __contains__(self, key):
        if Building.objects.filter(name=key):
            return True
        return False

buildings=BuildingsList()

def search(string):
  """
  search the buildings, then the floors, then the areas for occurence of [string],
  and return that object (or objects)
  """
  domain = deque()
  results = []
  #initialize queue with buildings
  for b in list(buildings):
    domain.appendleft(b)
  while domain:
    current = domain.pop()
    if string in current.name:
      results.append(current)
    if hasattr(current,'floors'):
      for f in list(current.floors.all()):
        domain.appendleft(f)
    #maybe buildings will have areas too, so this is `if` instead of `elif`
    if hasattr(current,'areas'):
      for a in list(current.areas.all()):
        domain.appendleft(a)
  return results

