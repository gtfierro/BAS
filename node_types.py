import json
from copy import deepcopy

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
    'objects': {
      'AHU': {
        'interface' : 'IAHU',
        'required_setpoints'  : ['ZON_AIR_STP_CMD'], 
        'required_points'     : ['OUT_AIR_DMP', 'OUT_AIR_TMP_SEN', 'MIX_AIR_TMP_SEN', 'RET_FAN', 'RET_AIR_FLW_SEN',
                                 'EXH_AIR_DMP', 'RET_AIR_HUM_SEN', 'RET_AIR_TMP_SEN', 'RET_AIR_DMP', 'RET_AIR_PRS_SEN',
                                 'COO_VLV', 'SUP_AIR_FAN', 'SUP_AIR_FLW_SEN','SUP_AIR_TMP_SEN','SUP_AIR_PRS_SEN'],
        },
      'CWL': {
        'interface':  'ICWL',
        'required_setpoints'  : ['CHL_WAT_PRS_DIF_STP'],
        'required_points'     : ['CON_WAT_COO_TOW','CON_WAT_SUP_TMP_SEN','CON_WAT_PMP','CON_CHL_WAT_CHR',
                                 'CON_WAT_RET_TMP_SEN','CHL_WAT_SUP_TMP_SEN','CHL_WAT_RET_TMP_SEN',
                                 'CHL_WAT_PMP','CHL_WAT_PRS_DIF_SEN'],
        },
      'HWL': {
        'interface' : 'IHWL',
        'required_setpoints'  : ['HOT_WAT_RET_TMP_STP','HOT_WAT_PRS_DIF_STP','HOT_WAT_SUP_TMP_STP'], 
        'required_points' : ['HX','HOT_WAT_RET_TMP_SEN','HOT_WAT_PRS_DIF_SEN','HOT_WAT_PMP','HOT_WAT_SUP_TMP_SEN'],
        },
      },

    'points': {
      'FAN': {
        'driver' : 'DFAN',
        'required_setpoints'  : ['SPD'],
        'required_points' : ['POW'],
        },
      'CCV':  {
        'driver' : 'DCCV',
        'required_setpoints'  : [], # % open?
        'required_points' : [],
        },
      'DMP':  {
        'driver' : 'DDMP',
        'required_setpoints'  : [], # % open?
        'required_points' : [],
        },
      'SEN' : {
        'driver' : 'DSEN',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'CHR' : {
        'driver' : 'DCHR',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'PMP' : {
        'driver' : 'DPMP',
        'required_setpoints'  : [],
        'required_points' : [],
       },
      'TOW' : {
        'driver' : 'DTOW',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'VLV' : {
        'driver' : 'DVLV',
        'required_setpoints'  : [],
        'required_points' : [],
        },
      'HX'  : {
        'driver' : 'DHX',
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
    }


def export_json():
  """
  Fix up the type_dict for exporting to JSON. This means changing the interface references
  to their string representations
  """
  tmp_dict = deepcopy(type_dict)
#  for ot in tmp_dict.iterkeys():
#    tmp_dict[ot]['interface'] = tmp_dict[ot]['interface']
#    for nt in tmp_dict[ot]['allowed_types'].iterkeys():
#      tmp_dict[ot]['allowed_types'][nt]['interface'] = tmp_dict[ot]['allowed_types'][nt]['interface'].__name__
  return json.dumps(tmp_dict)

def import_json(j):
  """
  We just take in the JSON-formatted dict, but for all 'interface's, we have to use getattr
  to replace the value in the dict with the actual interface reference
  """
  import interfaces
  tmp_dict= json.loads(j)
#  for ot in tmp_dict.iterkeys():
#    tmp_dict[ot]['interface'] = getattr(interfaces, tmp_dict[ot]['interface'])
#    for nt in tmp_dict[ot]['allowed_types'].iterkeys():
#      tmp_dict[ot]['allowed_types'][nt]['interface'] = getattr(interfaces, tmp_dict[ot]['allowed_types'][nt]['interface'])
  return tmp_dict

def get_interface(s):
  """ Get the interface for a given string, e.g. 'AHU' """
  import interfaces
  return getattr(interfaces, type_dict['objects'][s]['interface'])

def list_interfaces():
  """ Returns a list of all supported interfaces identified in type_dict """
  ifaces = []
  for obj in type_dict['objects'].iterkeys():
    ifaces.append(get_interface(obj))
  return ifaces

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



