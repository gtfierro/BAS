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

class AreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        self.fields['Floor'] = forms.ChoiceField(choices = Floor.objects.all())

    buildings = MapField([
      InfoLayerField([(get_ewkt(p.polygon), p.name) for p in Building.objects.all()],
                     {'name': 'Current Buildings'}),
      ], template = 'olwidget/admin_olwidget.html'
      )
    coordinates = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Area

class AreaAdmin(admin.ModelAdmin):
    model = Area
    form = AreaForm
    readonly_fields = ('image_tag', )
    class Media:
        js = (
            '/static/scripts/bas.admin.js',
            '/static/scripts/jquery.geo.min.js',
        )

class FloorForm(forms.ModelForm):
    buildings = MapField([
      InfoLayerField([(get_ewkt(p.polygon), p.name) for p in Building.objects.all()],
                     {'name': 'Current Buildings'}),
      ], template = 'olwidget/admin_olwidget.html'
      )

    class Meta:
        model = Floor

class FloorAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag', )
    form = FloorForm

admin.site.register([Building, Node], GoogleMapsAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Area, AreaAdmin)
