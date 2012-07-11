#!/bin/bash
spatialite geodjango.db "SELECT InitSpatialMetaData();"
python manage.py syncdb
echo 'Loading SDH lighting data ...'
python manage.py loadjson ../../data/sdh-lighting.json
echo 'Loading SDH hvac data ...'
python manage.py loadjson ../../data/sdh-floor4-hvac.json
