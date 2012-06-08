#TODO: have bacnet_classes use this to validate the creation of objects/nodes
#TODO: validation methods
import zope.interface
import json
from interfaces import *
from copy import deepcopy

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
            "AH": {                                         #type declaration for BObj
                  "name": "Air Handler",                    #what the type means
                  "interface": IAH,                         #reference to the interface we need to implement
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

