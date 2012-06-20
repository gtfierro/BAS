import node
import node_types
import requests
import json
from zope.interface import implements

from smap_wrapper import read_point, write_multiple_points
ROOT='http://127.0.0.1:8080/data/WattStopper'
#
#class BacNetFAN(node.Point):
#  implements(node_types.get_interface('AH.FAN'))
#
#class BacNetCCV(node.Point):
#  implements(node_types.get_interface('AH.CCV'))
#
#class BacNetDMP(node.Point):
#  implements(node_types.get_interface('AH.DMP'))
#
#class BacNetSEN(node.Point):
#  implements(node_types.get_interface('AH.SEN'))
#
#class BacNetCWL(node.Obj):
#  implements(node_types.get_interface('CWL'))
#
#class BacNetCH(node.Point):
#  implements(node_types.get_interface('CWL.CH'))
#
#class BacNetPU(node.Point):
#  implements(node_types.get_interface('CWL.PU'))
#
#class BacNetCT(node.Point):
#  implements(node_types.get_interface('CWL.CT'))
#
#class BacNetVV(node.Point):
#  implements(node_types.get_interface('CWL.VV'))
#
#class BacNetHWL(node.Point):
#  implements(node_types.get_interface('HWL'))
#
#class BacNetHX(node.Point):
#  implements(node_types.get_interface('HWL.HX'))


class BACnetREL(node.Point):
  implements(node_types.get_interface('REL'))

  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

  def get_json(self, value):
      return json.dumps({self.point: {'type': 'enumerated', 'value': value}})
 
  def set_brightness(self, value):
    requests.post(ROOT+'/write',self.get_json(value))

  def get_brightness(self):
    time, reading = requests.get(ROOT + self.point).json['Readings'][-1]
    return reading
