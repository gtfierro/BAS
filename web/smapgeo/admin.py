from smapgeo.models import Building, Floor, View, Area, AreaMetadata, NodeLink
from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin

#class OSMAdmin(admin.OSMGeoAdmin):
#	zoom_level = 8
#	default_lat = 37.871775
#	default_lon = -122.274603

class GoogleMapsAdmin(GeoModelAdmin):
    options = {
        'layers': ['google.streets'],
        'default_lat': 37.871775,
        'default_lon': -122.274603,
    }

#admin.site.register([Building, Floor, View, Area], OSMAdmin)
admin.site.register([Building, Floor, View, Area, AreaMetadata, NodeLink], GoogleMapsAdmin)

