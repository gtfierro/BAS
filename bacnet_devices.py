import node
import node_types
import requests
import json
from zope.interface import implements

ROOT='http://127.0.0.1:8080/data/WattStopper'

def read_point(point, root=ROOT):
  time, reading = requests.get(root + point).json['Readings'][-1]
  return reading

def write_point(point, value, type=None, root=ROOT):
    if type:
        write_multiple_points({point: {'type': type, 'value': value}})
    else:
        write_multiple_points({point: {'value': value}})

def write_multiple_points(data, root=ROOT):
    requests.post(root+'/write', json.dumps(data))


class BACnetFAN(node.Device):
  implements(node_types.get_device_interface('FAN'))

  # required_setpoints = ['SPD']
  # required_points = ['POW']
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetCCV(node.Device):
  implements(node_types.get_device_interface('CCV'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetDMP(node.Device):
  implements(node_types.get_device_interface('DMP'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetSEN(node.Device):
  implements(node_types.get_device_interface('SEN'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetCHR(node.Device):
  implements(node_types.get_device_interface('CHR'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetPMP(node.Device):
  implements(node_types.get_device_interface('PMP'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetTOW(node.Device):
  implements(node_types.get_device_interface('TOW'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetVLV(node.Device):
  implements(node_types.get_device_interface('VLV'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetHX(node.Device):
  implements(node_types.get_device_interface('HX'))
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point


class BACnetREL(node.Device):
  implements(node_types.get_device_interface('REL'))

  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

  def set_brightness(self, value):
    write_point(self.point, value, type='enumerated')

  def get_brightness(self):
    return read_point(self.point)
