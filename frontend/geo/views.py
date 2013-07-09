from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, {
        'url_prefix' : '/webapi/',
        'geo_prefix' : '/smapgeo/'
        })
    return HttpResponse(t.render(c))
