#TODO: write this file?
# use zope.interface to create abstracts for the supported types
#TODO: have bacnet_classes use this to validate the creation of objects/nodes

import zope.interface

class IAH(zope.interface.Interface):
  """
  Interface for all Air Handler objects (type AH)

  For all objects that implement this, we probably want some sort of
  assert obj.type == "AH"
  """

  #high level methods will take form of:
  #def high_level_method(arg, arg, arg):
  # stuff
  # here
  # -> don't need to use "self" bc of how zope works

  pass

class ICWL(zope.interface.Interface):
  """
  Interface for all Chilled Water Loop objects (type CWL)
  """
  pass

class IHWL(zope.interface.Interface):
  """
  Interface for all Hot Water Loop objects (type HWL)
  """
  pass

"""
type_dict defines the allowed types of objects, and the allowed types of nodes
for each of those objects. There's some redundancy
"""
type_dict = {
            "AH": {
                  "name": "Air Handler",
                  "interface": IAH,
                  "allowed_types": {
                                    "FAN" : "Fan",
                                    "CCV" : "Cooling Coil",
                                    "DMP" : "Damper",
                                    "SEN" : "Sensor"
                                   }
                  },
            "CWL": {
                    "name": "Chilled Water Loop",
                    "interface":ICWL,
                    "allowed_types": {
                                      "CH"  : "Chiller",
                                      "PU"  : "Pump",
                                      "CT"  : "Cooling Tower",
                                      "VV"  : "Valve",
                                      "SEN" : "Sensor"
                                     }
                   },
            "HWL": {
                    "name": "Hot Water Loop",
                    "interface":IHWL,
                    "allowed_types": {
                                      "HX"  : "Heat Exchanger",
                                      "PU"  : "Pump",
                                      "VV"  : "Valve",
                                      "SEN" : "Sensor"
                                     }
                   }
            }

