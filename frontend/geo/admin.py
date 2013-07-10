from geo.models import Building, Floor, Area, Node
from django.contrib.gis import admin
from django import forms
from olwidget.admin import GeoModelAdmin
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.utils import get_ewkt

class GoogleMapsAdmin(GeoModelAdmin):
    options = {
      'layers': ['google.streets'],
      'default_lat': 37.870218,
      'default_lon': -122.259481,
      'default_zoom' : 15,
      }

class FloorForm(forms.ModelForm):
    buildings = MapField([
      InfoLayerField([(get_ewkt(p.polygon), p.name) for p in Building.objects.all()],
                     {'name': 'Current Buildings'}),
      ], template = 'olwidget/admin_olwidget.html'
      )

    class Meta:
        model = Floor

class FloorAdmin(admin.ModelAdmin):
    form = FloorForm

admin.site.register([Building, Area, Node], GoogleMapsAdmin)
admin.site.register(Floor, FloorAdmin)
