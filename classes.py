"""
Contains the pre-implemented logic for the higher level objects like the AHU, HWL, CWL.
Each of these classes should be initialized with the specific instantiations of drivers that
they expect in order to provide the full functionality of the class. The drivers they expect can 
be found in node_types.get_required_setpoints('AHU'), node_types.get_required_points('AHU'), etc
"""
import sys
import node
import node_types
from zope.interface import implements

#try:
#  import bacnet_drivers
#except:
#  #bacnet_drivers do not correctly implement interfaces
#  sys.exit(0)

def validate(obj, points):
  """
  If the object that calls this this an object, then we look at the list of self._nk.nodes
  to make sure that we have all required points and set points there
  If the object that calls this is a point, then we look at the attributes and make sure
  that all required points/setpoitns are there
  """
  if isinstance(obj, node.Obj):
    #check obj._nk.nodes to make sure everything from node_types is there
    try:
      required_points = node_types.get_required_points(obj.__class__.__name__)
    except:
      print "No list of required points for %s in node_types.type_dict['objects'][%s]" % (obj.__class__.__name__, obj.__class__.__name__)
      required_points = None
  elif isinstance(obj, node.Point):
    #check obj.attributes
    try:
      required_points = nodes_types.get_required_points(obj.__class__.__name__)
    except:
      print "No list of required points for %s in node_types.type_dict['points'][%s]" % (obj.__class__.__name__, obj.__class__.__name__)
      required_points = None
  #now make sure that all points in required_points are in the points dict
  if not required_points:
    raise NotImplementedError
  for reqpt in required_points:
    if reqpt not in points.keys():
      raise NotImplementedError(reqpt+" is not provided")
  return points


class AHU(node.Obj):
  """
  Logic for Air Handlers
  """

  def __init__(self, container, name, devices):
    """
    [devices] should be a dictionary mapping the expected points in node_types.get_required_points()
    to the device instantiations from bacnet_devices (or whatever)
    """
    self.points = validate(self, devices)
    node.Obj.__init__(self,container, name, self.points.values())

  def get_airflow():
    pass

  def set_airflow():
    pass

  def set_zone_temp():
    pass

class CWL(node.Obj):
  pass

class HWL(node.Obj):
  pass


class LIG(node.Obj):

  def __init__(self,container, name, devices):
    """
    Devices is a dictionary of mappings from required points to instantiations of them
    e.g. {'relay_low':BACnetREL('low relay','/WS86007/RELAY05'),
          'relay_hi' :BACnetREL('hi relay','/WS86007/RELAY06')}
    """
    self.points = validate(self, devices)
    node.Obj.__init__(self,container, name, self.points.values())

  def get_relays(self):
    return filter(lambda x: x.type == "REL", self._nk.nodes())

  def get_level(self):
    """
    Retrieves the current level of the light.
    """
    low, high = self.get_relays()
    low_value = int(low.get_brightness())
    high_value = int(high.get_brightness())
    return low_value + 2*high_value

  def set_level(self, level):
    """
    Sets the level of the light.
    """
    low, high = self.get_relays()
    low.set_brightness(level % 2)
    high.set_brightness(level // 2)
