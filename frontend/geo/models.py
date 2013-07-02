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

class Area(models.Model, Serializable):
    name = models.CharField(max_length=50, unique=True)
    polygon = models.PolygonField()
    Floor = models.ForeignKey(Floor, related_name='areas')
