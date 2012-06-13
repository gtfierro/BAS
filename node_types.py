#TODO: have bacnet_classes use this to validate the creation of objects/nodes
#TODO: validation methods
from interfaces import *
import json
from copy import deepcopy

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
            "AH": {                                         #type declaration for BObj
                  "name": "Air Handler",                    #what the type means
                  "interface": IAH,                         #reference to the interface we need to implement
                  "required_tags": ['DIS_AIR_TMP_SEN','DIS_AIR_FAN_SPD_CMD','RET_AIR_FAN_SPD_CMD', # list of required tags for lookup dict
                                    'MIX_AIR_TMP_SEN','ZON_AIR_TMP_SEN','ZON_AIR_SPT_CMD','OUT_AIR_DMP_CMD',
                                    'EXH_AIR_DMP_CMD'],
                  "optional_tags": ['DIS_AIR_HUM_SEN','DIS_AIR_PRS_SEN','DIS_AIR_FLW_SEN','DIS_AIR_FAN_POW_SEN', # list of optional tags for lookup dict
                                    'RET_AIR_TMP_SEN','RET_AIR_HUM_SEN','RET_AIR_PRS_SEN','RET_AIR_FLW_SEN',
                                    'RET_AIR_CO2_SEN','RET_AIR_FAN_POW_SEN','ZON_AIR_HUM_SEN','ZON_AIR_CO2_SEN',
                                    'OUT_AIR_TMP_SEN','OUT_AIR_HUM_SEN','OUT_AIR_PRS_SEN','OUT_AIR_FLW_SEN',
                                    'OUT_AIR_FLW_STP_CMD','EXH_AIR_FAN_CMD'],
                  "allowed_types": {                        #allowed types for this object's nodes
                                    "FAN" : {                           #type declaration for BNode
                                              "name"      : "Fan",      #what the type means
                                              "interface" : IFAN        #reference to the interface we need to implement
                                            },
                                    "CCV" : {
                                              "name"      : "Cooling Coil",
                                              "interface" : ICCV
                                            },
                                    "DMP" : {
                                              "name"      : "Damper",
                                              "interface" : IDMP
                                            },
                                    "SEN" : { 
                                              "name"      : "Sensor",
                                              "interface" : ISEN
                                            }
                                   }
                  },
            "CWL": {
                    "name": "Chilled Water Loop",
                    "interface":ICWL,
                    "allowed_types": {
                                      "CH"  : {
                                                "name"     :  "Chiller",
                                                "interface":  ICH
                                              },
                                      "PU"  : {
                                                "name"      : "Pump",
                                                "interface" : IPU
                                              },
                                      "CT"  : {
                                                "name"      : "Cooling Tower",
                                                "interface" : ICT
                                              },
                                      "VV"  : {
                                                "name"      : "Valve",
                                                "interface" : IVV
                                              },
                                      "SEN" : {
                                                "name"      : "Sensor",
                                                "interface" : ISEN
                                              },
                                     }
                   },
            "HWL": {
                    "name": "Hot Water Loop",
                    "interface":IHWL,
                    "allowed_types": {
                                      "HX"  : {
                                                "name"      : "Heat Exchanger",
                                                "interface" : IHX
                                              },
                                      "PU"  : {
                                                "name"      : "Pump",
                                                "interface" : IPU
                                              },
                                      "VV"  : {
                                                "name"      : "Valve",
                                                "interface" : IVV
                                              },
                                      "SEN" : {
                                                "name"      : "Sensor",
                                                "interface" : ISEN
                                              },
                                     }
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
    }


def export_json():
  """
  Fix up the type_dict for exporting to JSON. This means changing the interface references
  to their string representations
  """
  tmp_dict = deepcopy(type_dict)
  for ot in tmp_dict.iterkeys():
    tmp_dict[ot]['interface'] = tmp_dict[ot]['interface'].__name__
    for nt in tmp_dict[ot]['allowed_types'].iterkeys():
      tmp_dict[ot]['allowed_types'][nt]['interface'] = tmp_dict[ot]['allowed_types'][nt]['interface'].__name__
  return json.dumps(tmp_dict)

def import_json(j):
  """
  We just take in the JSON-formatted dict, but for all 'interface's, we have to use getattr
  to replace the value in the dict with the actual interface reference
  """
  import interfaces
  tmp_dict= json.loads(j)
  for ot in tmp_dict.iterkeys():
    tmp_dict[ot]['interface'] = getattr(interfaces, tmp_dict[ot]['interface'])
    for nt in tmp_dict[ot]['allowed_types'].iterkeys():
      tmp_dict[ot]['allowed_types'][nt]['interface'] = getattr(interfaces, tmp_dict[ot]['allowed_types'][nt]['interface'])
  return tmp_dict

def get_interface(s):
  """ Get the interface for a given string, e.g. 'AH' or 'AH.FAN' """
  keys = s.split('.')
  if len(keys) == 1:
      return type_dict[keys[0]]['interface']
  elif len(keys) == 2:
      return type_dict[keys[0]]['allowed_types'][keys[1]]['interface']

def get_tag_name(tag):
  """ convert something like DIS_AIR_TMP_SEN to Discharge Air Temp Sensor """
  #convert tag to a list 
  tag = tag.split("_") if "_" in tag else [tag]
  classification = [abbreviations[prefix] for prefix in tag]
  return " ".join(classification)


