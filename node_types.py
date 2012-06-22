import json
from copy import deepcopy

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
    'objects': {
      'AHU': {
        'required_setpoints'  : ['ZON_AIR_STP_CMD'], 
        'required_points'     : ['OUT_AIR_DMP', 'OUT_AIR_TMP_SEN', 'MIX_AIR_TMP_SEN', 'RET_FAN', 'RET_AIR_FLW_SEN',
                                 'EXH_AIR_DMP', 'RET_AIR_HUM_SEN', 'RET_AIR_TMP_SEN', 'RET_AIR_DMP', 'RET_AIR_PRS_SEN',
                                 'COO_VLV', 'SUP_AIR_FAN', 'SUP_AIR_FLW_SEN','SUP_AIR_TMP_SEN','SUP_AIR_PRS_SEN'],
        },
      'CWL': {
        'required_setpoints'  : ['CHL_WAT_PRS_DIF_STP'],
        'required_points'     : ['CON_WAT_COO_TOW','CON_WAT_SUP_TMP_SEN','CON_WAT_PMP','CON_CHL_WAT_CHR',
                                 'CON_WAT_RET_TMP_SEN','CHL_WAT_SUP_TMP_SEN','CHL_WAT_RET_TMP_SEN',
                                 'CHL_WAT_PMP','CHL_WAT_PRS_DIF_SEN'],
        },
      'HWL': {
        'required_setpoints'  : ['HOT_WAT_RET_TMP_STP','HOT_WAT_PRS_DIF_STP','HOT_WAT_SUP_TMP_STP'], 
        'required_points' : ['HX','HOT_WAT_RET_TMP_SEN','HOT_WAT_PRS_DIF_SEN','HOT_WAT_PMP','HOT_WAT_SUP_TMP_SEN'],
        },
      'VAV': {
        'required_setpoints'  : [],
        'required_points'     : ['EXH_AIR_FAN'],
        },
      'LIG': {
        'required_setpoints'  : [],
        'required_points'     : ['HI_REL','LO_REL'],
        },
      },

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

def export_json():
  """
  Fix up the type_dict for exporting to JSON. This means changing the interface references
  to their string representations
  """
  tmp_dict = deepcopy(type_dict)
  return json.dumps(tmp_dict)

def import_json(j):
  """
  We just take in the JSON-formatted dict, but for all 'interface's, we have to use getattr
  to replace the value in the dict with the actual interface reference
  """
  import interfaces
  tmp_dict= json.loads(j)
  return tmp_dict

def get_interface(s):
  """ Get the interface for a given string, e.g. 'AHU' """
  import drivers
  return getattr(drivers, type_dict['points'][s]['interface'])

def list_interfaces():
  """ Returns a list of all supported interfaces identified in type_dict """
  ifaces = []
  for obj in type_dict['points'].iterkeys():
    ifaces.append(get_interface(obj))
  return ifaces

def list_tags(targ=''):
  """ Returns a list of all tags"""
  tags = []
  for o in type_dict['objects']:
    if not targ:
      tags.extend(type_dict['objects'][o]['required_points'])
    elif o == targ:
      tags.extend(type_dict['objects'][o]['required_points'])
  for p in type_dict['points']:
    if not targ:
      tags.extend(type_dict['points'][p]['required_points'])
    elif p == targ:
      tags.extend(type_dict['points'][p]['required_points'])
  return tags

def list_types():
  """ Returns a list of all types"""
  types = []
  types.extend(type_dict['objects'].keys())
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
  if s in type_dict['objects'].keys():
    return type_dict['objects'][s]['required_setpoints']
  else:
    return type_dict['points'][s]['required_setpoints']

def get_required_points(s):
  """ Return list of required points for a given string e.g. 'AH' """
  if s in type_dict['objects'].keys():
    return type_dict['objects'][s]['required_points']
  else:
    return type_dict['points'][s]['required_points']



