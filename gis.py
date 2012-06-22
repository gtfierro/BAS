import sys, os
sys.path.append(os.path.abspath('./geo'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from smapgeo.models import *
