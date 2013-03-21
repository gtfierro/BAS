import node
import device_types
import requests
import json
from zope.interface import implements

ROOT='http://127.0.0.1:8080/'
# Port forwarding:  ssh -L 8081:localhost:8080 user@<ip>
ROOT_SIEMENS=ROOT#'http://127.0.0.1:8080/data/Siemens'
ROOT_BANCROFT=ROOT#'http://127.0.0.1:8080/data/Bancroft'

def read_point(point, root=ROOT):
  time, reading = requests.get(root + str(point)).json()['Readings']
  return reading

def write_point(point, value, root=ROOT):
    res = requests.put(root + str(point) + '?state='+str(value))
    return res

class BACnetFAN(node.Device):
  implements(device_types.DFAN)

  # required_setpoints = ['SPD']
  # required_points = ['POW']
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

class BancroftFAN(node.Device):
  implements(device_types.DFAN)

  def __init__(self, name, point_spd, point_pow=None, uid=None):
    node.Device.__init__(self, name, uid=uid)
    self.point_spd = point_spd
    self.point_pow = point_pow

class BACnetCCV(node.Device):
  implements(device_types.DCCV)
  def __init__(self, name, point):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

class BACnetDMP(node.Device):
  implements(device_types.DDMP)
  def __init__(self, name, point, setpoint=None, uid=None):
      node.Device.__init__(self, name, uid=uid)
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

class BancroftVAVDMP(node.Device):
  implements(device_types.DDMP)

  def __init__(self, name, point, setpoint=None, uid=None):
    node.Device.__init__(self, name, uid=uid)
    self.device_id = point
    self.setpoint = setpoint
    self.point = point

  def get_percent_open(self):
    #point is something like device240202/flow_tab_1
    return read_point(self.point+'/DAMPER_OUTPUT',root=ROOT_BANCROFT)

  def set_percent_open(self, value):
    return write_point(self.point+'/DAMPER_LOCK',value, type='real',root=ROOT_BANCROFT)

class BancroftAHUDMP(node.Device):
  implements(device_types.DDMP)

  def __init__(self, name, point, setpoint=None, uid=None):
    node.Device.__init__(self, name, uid=uid)
    self.device_id = point
    self.setpoint = setpoint
    self.point = point

  def get_percent_open(self):
    #point is something like device240202/flow_tab_1
    return read_point(self.point,root=ROOT_BANCROFT)

  def set_percent_open(self, value):
    return write_point(self.point, value, type='real',root=ROOT_BANCROFT)

class BACnetSEN(node.Device):
  implements(device_types.DSEN)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

  def read(self, raw=False):
      if raw:
        print """bacnet.read_prop(self.h_dev, bacnet.OBJECT_ANALOG_OUTPUT, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, array_index=3)"""
      return read_point(self.uid,root=ROOT_SIEMENS)

class BancroftSEN(node.Device):
  implements(device_types.DSEN)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

  def read(self, raw=False):
      if raw:
        print """bacnet.read_prop(self.h_dev, bacnet.OBJECT_ANALOG_OUTPUT, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, array_index=3)"""
      return read_point(self.uid,root=ROOT_BANCROFT)


class BACnetCHR(node.Device):
  implements(device_types.DCHR)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

class BACnetPMP(node.Device):
  implements(device_types.DPMP)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

class BACnetTOW(node.Device):
  implements(device_types.DTOW)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

class BACnetVLV(node.Device):
  implements(device_types.DVLV)
  def __init__(self, name, point, setpoint=None, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point
      self.setpoint = setpoint

  def get_percent_open(self, raw=False):
      if raw:
        print """bacnet.read_prop(self.h_dev, bacnet.OBJECT_ANALOG_OUTPUT, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, array_index=3)"""
      return float(read_point(self.uid))

  def set_percent_open(self, value, raw=False):
      if self.setpoint is not None:
          if raw:
            print """bacnet.write_prop(self.h_dev, bacnet.OBJECT_ANALOG_VALUE, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, value=value, value_type=bacnet.BACNET_APPLICATION_TAG_REAL)"""
          write_point(self.setpoint.uid, value, type='real')
      else:
          return "No setpoint given"

class BACnetHX(node.Device):
  implements(device_types.DHX)
  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point


class BACnetREL(node.Device):
  implements(device_types.DREL)

  def __init__(self, name, point, uid=None):
      node.Device.__init__(self, name, uid=uid)
      self.point = point

  def set_brightness(self, value, raw=False):
      if raw:
        print """ bacnet.write_prop(self, object_type=bacnet.OBJECT_BINARY_OUTPUT, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, value=value, value_type=bacnet.BACNET_APPLICATION_TAG_REAL)"""
      write_point(self.uid, value)

  def get_brightness(self, raw=False):
      if raw:
        print """bacnet.read_prop(self.h_dev, bacnet.OBJECT_BINARY_VALUE, instance_number=self.instance_number, property=bacnet.PROP_PRESENT_VALUE, array_index=3)"""
      return float(read_point(self.uid))
