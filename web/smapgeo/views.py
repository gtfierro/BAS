from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from models import Building
from svg import building_to_svg, svg_to_building
from django import forms
import json
import os

def floorplan(request, name):
  path = os.path.join(settings.SMAPGEO_DATA_DIR, 'floor_plans/', name + '.png')
  with open(path, "rb") as f:
    return HttpResponse(f.read(), mimetype="image/png")

def index(request):
    t = loader.get_template('select_building.html')
    c = Context({
        'heading' : 'Buildings',
        'url_prefix' : '/smapgeo/',
        'buildings' : Building.objects.all()
        })
    return HttpResponse(t.render(c))

def building_svg(request, building_id):
    try:
        b = Building.objects.get(id=building_id)
    except:
        return HttpResponse("Invalid Building")

    return HttpResponse(building_to_svg(b), mimetype='image/svg+xml')

def building_svg_params(request):
    if 'building' not in request.GET:
      return HttpResponseBadRequest("Invalid Building")
    building = request.GET.get('building')
    floor_names = request.GET.getlist('floors[]')
    types = request.GET.getlist('types[]')
    try:
        b = Building.objects.get(name=building)
    except:
        return HttpResponseNotFound("Building not found")

    return HttpResponse(building_to_svg(b, False, "http://127.0.0.1:8000", floor_names, types), mimetype='image/svg+xml')


def building_json(request, building_id):
    try:
        b = Building.objects.get(id=building_id)
    except:
        return HttpResponse("Invalid Building")

    return HttpResponse(b.dumps(), mimetype='application/json')

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def upload(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST': # If the form has been submitted...
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            if f.name.endswith('.json'):
                Building.loads(f.read())
            elif f.name.endswith('.svg'):
                svg_to_building(f.read())
            else:
                return HttpResponse("This file type is not supported")
            return HttpResponseRedirect("/smapgeo/")
    else:
        form = UploadFileForm()

    c['form'] = form
    return render_to_response('upload.html', c)
