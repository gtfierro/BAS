from geo.models import Building, Floor, Area, Node
from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin

#class OSMAdmin(admin.OSMGeoAdmin):
#   zoom_level = 8
#   default_lat = 37.871775
#   default_lon = -122.274603

class GoogleMapsAdmin(GeoModelAdmin):
    options = {
      'layers': ['google.streets'],
      'default_lat': 37.870218,
      'default_lon': -122.259481,
      'default_zoom' : 15,
      }

admin.site.register([Building, Floor, Area, Node], GoogleMapsAdmin)
