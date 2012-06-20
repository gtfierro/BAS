import node
import node_types
import requests
import json
from zope.interface import implements

from smap_wrapper import read_point, write_multiple_points
ROOT='http://127.0.0.1:8080/data/WattStopper'

class BACnetFAN(node.Point):
  implements(node_types.get_interface('FAN'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetCCV(node.Point):
  implements(node_types.get_interface('CCV'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetDMP(node.Point):
  implements(node_types.get_interface('DMP'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetSEN(node.Point):
  implements(node_types.get_interface('SEN'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetCHR(node.Point):
  implements(node_types.get_interface('CHR'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetPMP(node.Point):
  implements(node_types.get_interface('PMP'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetTOW(node.Point):
  implements(node_types.get_interface('TOW'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetVLV(node.Point):
  implements(node_types.get_interface('VLV'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point

class BACnetHX(node.Point):
  implements(node_types.get_interface('HX'))
  def __init__(self, name, point):
      node.Point.__init__(self, name)
      self.point = point


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
