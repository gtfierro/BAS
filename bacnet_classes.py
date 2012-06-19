import node
import node_types
from zope.interface import implements

from smap_wrapper import read_point, write_multiple_points

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

  def get_relays(self):
      low = [ pt for pt in self.nodes if pt.type == 'RELAY' and pt['type'] == 'low' ]
      high = [ pt for pt in self.nodes if pt.type == 'RELAY' and pt['type'] == 'high' ]
      return low[0], high[0]

  def get_level(self):
    """
    Retrieves the current level of the light.
    """
    low, high = self.get_relays()
    low_value = int(read_point(low['point']))
    high_value = int(read_point(high['point']))
    return low_value + 2*high_value

  def set_level(self, level):
    """
    Sets the level of the light.
    """
    low, high = self.get_relays()
    write_multiple_points({high['point']: dict(value=level % 2, type='enumerated'),
                            low['point']: dict(value=level // 2, type='enumerated')})


class BacNetRELAY(node.Point):
  implements(node_types.get_interface('LIGHT.RELAY'))

  def __init__(self, container, name, type, point):
      assert type in ('low', 'high')
      node.Point.__init__(self, container, name)
      self['type'] = type
      self['point'] = point
