from geo.models import Building, Floor, Area, Node
from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin

class GoogleMapsAdmin(GeoModelAdmin):
    options = {
      'layers': ['google.streets'],
      'default_lat': 37.870218,
      'default_lon': -122.259481,
      'default_zoom' : 15,
      }

admin.site.register([Building, Area, Node], GoogleMapsAdmin)
admin.site.register([Floor])
