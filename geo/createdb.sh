#!/bin/bash
spatialite geodjango.db "SELECT InitSpatialMetaData();"
python manage.py syncdb
