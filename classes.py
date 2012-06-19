"""
Contains the pre-implemented logic for the higher level objects like the AHU, HWL, CWL.
Each of these classes should be initialized with the specific instantiations of drivers that
they expect in order to provide the full functionality of the class. The drivers they expect can 
be found in node_types.get_required_setpoints('AHU'), node_types.get_required_points('AHU'), etc
"""
import node
import node_types
from zope.interface import implements

class DriverValidator(object):
  """
  Upon initalizing this class with a string that references the object in 
  node_types.type_dict['objects'], it validates the *drivers list of input points
  to make sure they are all of the supported type.

  For example, if we had an object Foo that had required_points of 'bar' and 'baz',
  we'd initialize our class below with DriverValidator('Foo','bar','baz'), which would
  only pass initialization if 'bar' and 'baz' were valid, which they are.
  """

  def __init__(self, type, *drivers):
    """
    [type] is a string describing one of the classes listed below that is *also* in
    node_types.type_dict['objects']
    [drivers] is a list of instantiated drivers that should cover the minimum set of points 
    provided by the object/point's required_setpoints, required_points
    """
    # get the required points
    self.required_setpoints = node_types.get_required_setpoints(type)
    self.required_points = node_types.get_required_points(type)

    # check the provided points against the provided minimum set 
    for driver in drivers:



class AHU(node.Obj):
  """
  Logic for Air Handlers
  """

  def get_airflow():
    pass

  def set_airflow():
    pass

  def set_zone_temp():
    pass


#TODO: plug in the expected points for this type
class Light(node.Obj):

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

