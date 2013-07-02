from django.contrib.gis.db import models
from django.conf import settings
from serialization import Serializable

# Create your models here.


class Building(models.Model, Serializable):
    name = models.CharField(max_length=50, unique=True)
    polygon = models.PolygonField()
    objects = models.GeoManager()

class Floor(models.Model, Serializable):
    name = models.CharField(max_length=50, unique=True)
    polygon = models.PolygonField()
    building = models.ForeignKey(Building, related_name='floors')
    objects = models.GeoManager()

class Area(models.Model, Serializable):
    name = models.CharField(max_length=50, unique=True)
    polygon = models.PolygonField()
    floor = models.ForeignKey(Floor, related_name='areas')
    objects = models.GeoManager()

class Node(models.Model, Serializable):
    smap_uuid = models.CharField(max_length=100, unique=True) # should I use a UUID field here?
    point = models.PointField()
    area = models.ForeignKey(Area, related_name='nodes')
    objects = models.GeoManager()
