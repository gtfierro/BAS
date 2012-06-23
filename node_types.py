import json
from copy import deepcopy

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
    'points': {
      'REL': {
        'interface' : 'DREL',
        'required_setpoints'  : [],
        'required_points'     : [],
        },
      'FAN': {
        'interface' : 'DFAN',
        'required_setpoints'  : ['SPD'],
        'required_points' : ['POW'],
        },
      'CCV':  {
        'interface' : 'DCCV',
        'required_setpoints'  : [], # % open?
        'required_points' : [],
        },
      'DMP':  {
        'interface' : 'DDMP',
        'required_setpoints'  : [], # % open?
        'required_points' : [],
        },
      'SEN' : {
        'interface' : 'DSEN',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'CHR' : {
        'interface' : 'DCHR',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'PMP' : {
        'interface' : 'DPMP',
        'required_setpoints'  : [],
        'required_points' : [],
       },
      'TOW' : {
        'interface' : 'DTOW',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'VLV' : {
        'interface' : 'DVLV',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'HX'  : {
        'interface' : 'DHX',
        'required_setpoints'  : [],
        'required_points' : [],
        },

    }
   }
abbreviations = {
    'DIS' : 'Discharge',
    'AIR' : 'Air',
    'TMP' : 'Temperature',
    'SEN' : 'Sensor',
    'SPD' : 'Speed',
    'CMD' : 'Point of Actuation',
    'RET' : 'Return',
    'MIX' : 'Mixed',
    'ZON' : 'Zone',
    'SPT' : 'Setpoint',
    'OUT' : 'Outside',
    'DMP' : 'Damper',
    'HUM' : 'Humidity',
    'PRS' : 'Pressure',
    'FLW' : 'Flow',
    'POW' : 'Power',
    'CO2' : 'Carbon Dioxide',
    'EXH' : 'Exhaust',
    'FAN' : 'Fan',
    'COO' : 'Cooling',
    'VLV' : 'Valve',
    'AHU' : 'Air Handler',
    'CCV' : 'Cooling Coil',
    'CWL' : 'Cold Water Loop',
    'HWL' : 'Hot Water Loop',
    'REL' : 'Relay',
    'HI'  : 'High',
    'LO'  : 'Low',
    'LIG' : 'Light',
    }

def get_interface(s):
  """ Get the interface for a given string, e.g. 'AHU' """
  import driver_types
  return getattr(driver_types, 'D' + s)

def list_interfaces():
  """ Returns a list of all supported interfaces identified in type_dict """
  import driver_types
  return [ getattr(driver_types, k) for k in driver_types.__dict__.keys() if k.isupper() and k.startswith('D') ]

def list_classes():
  import classes
  import node
  return [v for v in classes.__dict__.values() if type(v) == type and issubclass(v, node.Obj)]

def list_tags(targ=''):
  """ Returns a list of all tags"""
  tags = set()
  for cls in list_classes():
    tags |= set(cls.required_devices)
  for p in type_dict['points']:
    if not targ:
      tags |= set(type_dict['points'][p]['required_points'])
    elif p == targ:
      tags |= set(type_dict['points'][p]['required_points'])
  return list(tags)

def list_types():
  """ Returns a list of all types"""
  types = []
  types.extend(x.__name__ for x in list_classes())
  types.extend(type_dict['points'].keys())
  return types

def get_tag_name(tag):
  """ convert something like DIS_AIR_TMP_SEN to Discharge Air Temp Sensor """
  #convert tag to a list 
  tag = tag.split("_") if "_" in tag else [tag]
  classification = [abbreviations[prefix] for prefix in tag if prefix in abbreviations ]
  return " ".join(classification)

def get_required_setpoints(s):
  """ Return list of required setpoints for a given string e.g. 'AH' """
  import classes
  if s in classes.__dict__:
      return getattr(classes, s).required_setpoints
  else:
    return type_dict['points'][s]['required_setpoints']

def get_required_points(s):
  """ Return list of required points for a given string e.g. 'AH' """
  import classes
  if s in classes.__dict__:
      return getattr(classes, s).required_drivers
  else:
    return type_dict['points'][s]['required_points']



