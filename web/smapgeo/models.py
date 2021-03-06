from django.contrib.gis.db import models
from django.conf import settings
from copy import copy
from PIL import Image
from serialization import Serializable, py_to_dict
from inkscape import geoutil
from math import sqrt, asin, degrees
import os

def find_or_create(cls, save, **kwargs):
    try:
        return cls.objects.get(**kwargs)
    except:
        ret = cls(**kwargs)
        if save:
            ret.save()
        return ret

class NodeLink(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)

    def __unicode__(self):
        return self.uuid

class Building(models.Model, Serializable):
    name = models.CharField(max_length=50, unique=True)

    objects = models.GeoManager()

    class Meta:
        ordering = ['name']

    def __getitem__(self, key):
        floors = self.floors.filter(name=key)
        if len(floors) == 0:
            raise KeyError("Floor not found in building")
        else:
            return floors[0]

    def __setitem__(self, key, value):
        assert False

    def __contains__(self, key):
        return self.floors.filter(name=key).count() > 0

    def items(self):
        return [(x.name, x) for x in self.floors.all()]

    def __unicode__(self):
        return self.name

    def dict(self):
        return {
            'name': self.name,
            'floors': {x.name: x.dict() for x in self.floors.all()}
            }

    @classmethod
    def from_dict(cls, j, args=None):
        b = find_or_create(cls, True, name=str(j['name']))
        for name, fj in j['floors'].items():
            f = Floor.from_dict(fj, building=b, name=name)
        return b

    def __emittable__(self):
        """Dictionary representation for appstack web api"""
        return {
            'name': self.name,
            'type': 'Building'
            }

class Floor(models.Model, Serializable):
    name = models.CharField(max_length=50)
    building = models.ForeignKey(Building, related_name='floors')

    objects = models.GeoManager()

    class Meta:
        ordering = ['building', 'name']

    def __getitem__(self, key):
        areas = self.areas.filter(name=key)
        if len(areas) == 0:
            raise KeyError("Area not found in floor")
        else:
            return areas[0]

    def __setitem__(self, key, value):
        assert False

    def __contains__(self, key):
        return self.areas.filter(name=key).count() > 0

    def items(self):
        return [(x.name, x) for x in self.areas.all()]

    def get_view(self, key):
        views = self.views.filter(name=key)
        if len(views) == 0:
            raise KeyError("View not found in floor")
        else:
            return views[0]

    def set_view(self, key, value):
        assert False

    def __unicode__(self):
        return "{}:{}".format(self.building.name, self.name)

    def dict(self):
        return {
            'areas': py_to_dict(self),
            'views': {x.name: x.dict() for x in self.views.all()}
            }

    @classmethod
    def from_dict(cls, j, building, name, **kwargs):
        f = find_or_create(cls, True, building=building, name=name)
        for name, vj in j['views'].items():
            View.from_dict(vj, floor=f, name=name)
        for name, fj in j['areas'].items():
            Area.from_dict(fj, floor=f, name=name)
        return f

    def __emittable__(self):
        """Dictionary representation for appstack web api"""
        return {
            'name': self.name,
            'type': 'Floor',
            'building': self.building.name
            }

class View(models.Model, Serializable):
    name = models.CharField(max_length=25) # Computer id
    floor = models.ForeignKey(Floor, related_name='views')
    image = models.CharField(max_length=200, blank=True)
    rectangle = models.PolygonField()

    class Meta:
        ordering = ['floor', 'name']

    @property
    def dimensions(self):
        try:
            img = Image.open(os.path.join(settings.SMAPGEO_DATA_DIR, self.image))
            width, height = img.size
        except:
            print "ERROR: could not open image: " + self.image
            width, height = 1, 1
        return width, height

    @property
    def mtx(self):
        try:
            img = Image.open(os.path.join(settings.SMAPGEO_DATA_DIR, self.image))
            width, height = img.size
        except:
            width, height = 1, 1

        x, y = self.rectangle.coords[0][0]
        a, b = self.rectangle.coords[0][1]
        a -= x
        b -= y
        c, d = self.rectangle.coords[0][3]
        c -= x
        d -= y
        return [[a / width, c / height, x], [b / width, d / height, y]]
    @mtx.setter
    def mtx(self, value):
        width, height = self.dimensions
        polygon = [[value[0][2], value[1][2]]]
        polygon.append([polygon[0][0] + value[0][0] * width,
                        polygon[0][1] + value[1][0] * width])
        polygon.append([polygon[0][0] + value[0][0] * width + value[0][1] * height,
                        polygon[0][1] + value[1][0] * width + value[1][1] * height])
        polygon.append([polygon[0][0] + value[0][1] * height,
                        polygon[0][1] + value[1][1] * height])
        wkt = 'POLYGON(('
        for x, y in polygon:
            wkt += str(x)
            wkt += ' '
            wkt += str(y)
            wkt += ', '
        x, y = polygon[0]
        wkt += str(x)
        wkt += ' '
        wkt += str(y)
        wkt += '))'

        self.rectangle = wkt

    @property
    def latlonbox(self):
        # Three points on the rectangle
        x, y = self.rectangle.coords[0][0]
        a, b = self.rectangle.coords[0][1]
        c, d = self.rectangle.coords[0][3]

        # Half of the width/height vectors
        Ax = (a-x)/2
        Ay = (b-y)/2
        Bx = (c-x)/2
        By = (d-y)/2

        # Center of the rectangle
        Cx = x + Ax + Bx
        Cy = y + Ay + By

        A = sqrt(Ax**2 + Ay**2)
        B = sqrt(Bx**2 + By**2)

        return Cy + B, Cy - B, Cx + A, Cx - A, -degrees(asin(Ay/Ax))

    objects = models.GeoManager()

    def __unicode__(self):
        return "{}:{}:{}".format(self.floor.building.name,
                                 self.floor.name,
                                 self.name)

    def dict(self):
        return {
            'mtx': self.mtx,
            'image': self.image
            }

    @classmethod
    def from_dict(cls, j, floor, name, **kwargs):
        v = find_or_create(cls, False, floor=floor, name=name)
        v.image = j['image'] or ''
        v.mtx = j['mtx']
        v.save()
        return v

class Area(models.Model, Serializable):
    name = models.CharField(max_length=50)
    regions = models.MultiPolygonField()
    floor = models.ForeignKey(Floor, related_name='areas')
    nodes = models.ManyToManyField(NodeLink, related_name='areas', blank=True)

    class Meta:
        ordering = ['floor', 'name']

    @property
    def streams(self):
        '''Backwards compatibility for when we were linking against sMAP streams'''
        return self.nodes

    def get_regions(self, view=None):
        regions = [[[y[0], y[1]] for y in x[0]] for x in self.regions.coords]
        if view is not None:
            geoutil.applyTransformToRegions(geoutil.inverse(view.mtx),
                                            regions)
        return regions

    def set_regions(self, regions, view=None):
        r = copy(regions)
        if view is not None:
            geoutil.applyTransformToRegions(geoutil.inverse(view.mtx), r)

        wkt = 'MULTIPOLYGON('
        for polygon in regions:
            wkt += '(('
            for x, y in polygon:
                wkt += str(x)
                wkt += ' '
                wkt += str(y)
                wkt += ', '
            wkt = wkt[:-2]
            wkt += '))'
        wkt += ')'

        self.regions = wkt

    objects = models.GeoManager()

    def __unicode__(self):
        return "{}:{}:{}".format(self.floor.building.name, self.floor.name, self.name)

    def dict(self):
        return {
            'regions': self.get_regions(),
            'streams': [x.uuid for x in self.streams.all()],
            'metadata': {meta.tagname: meta.tagval for meta in self.metadata.all()}
            }

    @classmethod
    def from_dict(cls, j, floor, name, **kwargs):
        a = find_or_create(cls, False, floor=floor, name=name)
        a.set_regions(j['regions'])
        a.save()
        a.streams.clear()
        try:
            for streamuuid in j['streams']:
                a.streams.add(NodeLink.objects.get(uuid=streamuuid))
        except:
            pass

        try:
            for tag, value in j['metadata'].items():
                m = find_or_create(AreaMetadata, save=False, area=a, tagname=tag)
                m.tagval = value
                m.save()
        except KeyError:
            pass
        a.save()
        return a

    def __emittable__(self):
        """Dictionary representation for appstack web api"""
        return {
            'name': self.name,
            'type': 'Area',
            'floor': self.floor.name,
            'building': self.floor.building.name
            }

class AreaMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Area, related_name='metadata')
    tagname = models.CharField(max_length=64)
    tagval = models.TextField()

    objects = models.GeoManager()

    class Meta:
        ordering = ['area', 'tagname']
        verbose_name_plural = "area metadata"


    def __unicode__(self):
        return "{}.{}={}".format(self.area, self.tagname, self.tagval.split('\n')[0])
