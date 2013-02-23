from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from appstack import gis
import emitters

def login(request):
    c = RequestContext(request,{
        'url_prefix' : '/webapi/'
        })
    return render_to_response('login.html', context_instance=c)

@login_required
def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, {
        'url_prefix' : '/webapi/',
        'geo_prefix' : '/smapgeo/'
        })
    return HttpResponse(t.render(c))

@login_required
def geo(request):
    t = loader.get_template('geo.html')
    if 'building' not in request.GET:
        e = emitters.JSONEmitter(list(gis.buildings), {}, None)
        return HttpResponse(loader.get_template('objs.html').render(Context({
                        'url_prefix' : '/webapi/',
                        'objs': e.construct()
                    })))
    building_name = request.GET['building']
    if building_name not in gis.buildings:
        return HttpResponseBadRequest("Could not find building")
    building = gis.buildings[building_name]
    c = RequestContext(request,{
        'heading' : 'Buildings',
        'url_prefix' : '/webapi/',
        'geo_prefix' : '/smapgeo/',
        'building' : building
        })
    return HttpResponse(t.render(c))
