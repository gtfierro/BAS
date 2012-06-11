import node
import node_types
from zope.interface import implements

import bacnet_io

class BacNetAH(node.Obj):
  implements(node_types.get_interface('AH'))

class BacNetFAN(node.Point):
  implements(node_types.get_interface('AH.FAN'))

class BacNetCCV(node.Point):
  implements(node_types.get_interface('AH.CCV'))

class BacNetDMP(node.Point):
  implements(node_types.get_interface('AH.DMP'))

class BacNetSEN(node.Point):
  implements(node_types.get_interface('AH.SEN'))

class BacNetCWL(node.Obj):
  implements(node_types.get_interface('CWL'))

class BacNetCH(node.Point):
  implements(node_types.get_interface('CWL.CH'))

class BacNetPU(node.Point):
  implements(node_types.get_interface('CWL.PU'))

class BacNetCT(node.Point):
  implements(node_types.get_interface('CWL.CT'))

class BacNetVV(node.Point):
  implements(node_types.get_interface('CWL.VV'))

class BacNetHWL(node.Point):
  implements(node_types.get_interface('HWL'))

class BacNetHX(node.Point):
  implements(node_types.get_interface('HWL.HX'))

class BacNetLIGHT(node.Obj):
  implements(node_types.get_interface('LIGHT'))

  def _get_objs(self):
      low = [ pt['point'] for pt in self.nodes if pt.type == 'RELAY' and pt['type'] == 'low' ]
      high = [ pt['point'] for pt in self.nodes if pt.type == 'RELAY' and pt['type'] == 'high' ]
      return low[0], high[0]

  def _set_light(self, low_setting, high_setting, retries_left):
    """
    Checks current setting for lights and only writes to lights if the requested
    settings are different
    """
    if retries_left <= 0:
      return

    low_obj, high_obj = self._get_objs()

    current_setting = low_obj.read_point()
    if current_setting != int(low_setting):
      low_obj.read_point()
      low_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, low_setting)
      low_obj.read_point()
      low_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, low_setting)
      low_obj.read_point()
      low_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, low_setting)
    current_setting = high_obj.read_point()
    if current_setting != int(high_setting):
      high_obj.read_point()
      high_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, high_setting)
      high_obj.read_point()
      high_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, high_setting)
      high_obj.read_point()
      high_obj.write_point(bacnet_io.BACNET_APPLICATION_TAG_ENUMERATED, high_setting)

    #if the writes didn't work, try again
    if self.get_level() != (low_setting + 2 * high_setting):
      self._set_light(low_setting, high_setting, retries_left - 1)

  def get_level(self):
    """
    Retrieves the current level of the light. I tested this with combinations of
    actual wall switches and direct manipulation of BACnet, and this returned the
    correct light level each time!
    """
    low_obj, high_obj = self._get_objs()

    for i in range(2):
      low_obj.read_point(bacnet_io.PROP_PRIORITY_ARRAY)
      high_obj.read_point(bacnet_io.PROP_PRIORITY_ARRAY)
      low_obj.read_point(bacnet_io.PROP_PRIORITY_ARRAY)
      high_obj.read_point(bacnet_io.PROP_PRIORITY_ARRAY)
      low_obj.read_point() + 2*high_obj.read_point()

    return low_obj.read_point() + 2*high_obj.read_point()

  def set_level(self, level):
    retries = 2
    if level == 0:
      self._set_light(0, 0, retries)
    elif level == 1: 
      self._set_light(1, 0, retries)
    elif level == 2: 
      self._set_light(0, 1, retries)
    elif level == 3: 
      self._set_light(1, 1, retries)
    else:
      print "Unknown level", level


class BacNetRELAY(node.Point):
  implements(node_types.get_interface('LIGHT.RELAY'))

  def __init__(self, container, name, type, point):
      assert type in ('low', 'high')
      node.Point.__init__(self, container, name)
      self['type'] = type
      self['point'] = point
