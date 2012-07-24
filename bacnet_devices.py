import node
import device_types
import requests
import json
from zope.interface import implements

ROOT='http://127.0.0.1:8080/data/WattStopper'
# Port forwarding:  ssh -L 8081:localhost:8080 user@<ip>
ROOT_SIEMENS='http://127.0.0.1:8081/data/Siemens'
ROOT_BANCROFT='http://127.0.0.1:8082/data/Bancroft'

def read_point(point, root=ROOT):
  print root+point
  time, reading = requests.get(root + point).json['Readings'][-1]
  return reading

def write_point(point, value, type=None, root=ROOT):
    if type:
        write_multiple_points({point: {'type': type, 'value': value}}, root)
    else:
        write_multiple_points({point: {'value': value}}, root)

def write_multiple_points(data, root=ROOT):
    requests.post(root+'/write', json.dumps(data))


class BACnetFAN(node.Device):
  implements(device_types.DFAN)

  # required_setpoints = ['SPD']
  # required_points = ['POW']
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetCCV(node.Device):
  implements(device_types.DCCV)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetDMP(node.Device):
  implements(device_types.DDMP)
  def __init__(self, name, point, setpoint=None):
      node.Device.__init__(self, name)
      self.point = point
      self.setpoint = setpoint

  def get_percent_open(self):
      return read_point(self.point, root=ROOT_SIEMENS)

  def set_percent_open(self, value):
      if self.setpoint is not None:
          write_point(self.setpoint, value, type='real', root=ROOT_SIEMENS)
      else:
          return "No setpoint given"

#TODO: test this class

class BancroftDMP(node.Device):
  implements(device_types.DDMP)

  def __init__(self, name, point, setpoint=None):
    node.Device.__init__(self, name)
    self.device_id = point
    self.setpoint = setpoint
    self.point = point

  def get_percent_open(self):
    #point is something like device240202/flow_tab_1
    return read_point(self.point+'/DAMPER_OUTPUT',root=ROOT_BANCROFT)
 
  def set_percent_open(self, value):
    return write_point(self.point+'/DAMPER_LOCK',value, type='real',root=ROOT_BANCROFT)

class BACnetSEN(node.Device):
  implements(device_types.DSEN)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetCHR(node.Device):
  implements(device_types.DCHR)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetPMP(node.Device):
  implements(device_types.DPMP)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetTOW(node.Device):
  implements(device_types.DTOW)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

class BACnetVLV(node.Device):
  implements(device_types.DVLV)
  def __init__(self, name, point, setpoint=None):
      node.Device.__init__(self, name)
      self.point = point
      self.setpoint = setpoint

  def get_percent_open(self):
      return read_point(self.point, root=ROOT_SIEMENS)

  def set_percent_open(self, value):
      if self.setpoint is not None:
          write_point(self.setpoint, value, type='real', root=ROOT_SIEMENS)
      else:
          return "No setpoint given"

class BACnetHX(node.Device):
  implements(device_types.DHX)
  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point


class BACnetREL(node.Device):
  implements(device_types.DREL)

  def __init__(self, name, point):
      node.Device.__init__(self, name)
      self.point = point

  def set_brightness(self, value):
    write_point(self.point, value, type='enumerated')

  def get_brightness(self):
    return read_point(self.point)
