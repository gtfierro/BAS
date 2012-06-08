#TODO: have bacnet_classes use this to validate the creation of objects/nodes
#TODO: validation methods

import zope.interface
from interfaces import *

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

