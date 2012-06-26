from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/?$', 'smapgeo.views.index'),
    (r'^(?P<building_id>\w+).html$', 'smapgeo.views.building_html'),
    (r'^(?P<building_id>\w+).svg$', 'smapgeo.views.building_svg'),
    (r'^(?P<building_id>\w+).json$', 'smapgeo.views.building_json'),
    (r'^(?P<building_id>\w+).kml$', 'smapgeo.views.building_kml'),
    (r'^upload/$', 'smapgeo.views.upload'),
    (r'^floor_plans/(?P<name>\w+).png$', 'smapgeo.views.floorplan'),
)
