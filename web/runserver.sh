#!/bin/bash

## Cleanup old files
kill -9 $(cat dryrun.pid)
rm nohup.out

## Setup database
rm ../geodjango.db
spatialite geodjango.db "SELECT InitSpatialMetaData();"
python manage.py syncdb
echo 'Loading SDH lighting data ...'
python manage.py loadjson ../data/sdh-lighting.json
echo 'Loading SDH hvac data ...'
python manage.py loadjson ../data/sdh-floor4-hvac.json
echo 'Loading Bancroft Library hvac data...'
python manage.py loadjson ../data/bancroft-hvac.json
cd .. && ln -s web/geodjango.db .
cd -

## Start flask server
nohup python ../dryrun/dryrun.py & echo $! > dryrun.pid

## Start main server
python manage.py runserver
