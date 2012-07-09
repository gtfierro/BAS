#!/bin/bash
spatialite geodjango.db "SELECT InitSpatialMetaData();"
python manage.py syncdb
python manage.py loadjson ../../data/sdh-lighting.json
