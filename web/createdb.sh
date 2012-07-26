#!/bin/bash
rm ../geodjango.db
spatialite geodjango.db "SELECT InitSpatialMetaData();"
python manage.py syncdb
echo 'Loading SDH lighting data ...'
python manage.py loadjson ../../data/sdh-lighting.json
echo 'Loading SDH hvac data ...'
python manage.py loadjson ../../data/sdh-floor4-hvac.json
echo 'Loading Bancroft Library hvac data...'
python manage.py loadjson ../../data/bancroft-hvac.json
cd .. && ln -s web/geodjango.db .
