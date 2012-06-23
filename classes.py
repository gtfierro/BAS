"""
Contains the pre-implemented logic for the higher level objects like the AHU, HWL, CWL.
Each of these classes should be initialized with the specific instantiations of drivers that
they expect in order to provide the full functionality of the class. The drivers they expect can 
be found in node_types.get_required_setpoints('AHU'), node_types.get_required_points('AHU'), etc
"""
import sys
import node
import node_types
import interfaces
import inspect
from zope.interface import implements
from zope.schema import getValidationErrors

# def validate(obj, points):
#   """
#   If the object that calls this this an object, then we look at the list of self._nk.nodes
#   to make sure that we have all required points and set points there
#   If the object that calls this is a point, then we look at the attributes and make sure
#   that all required points/setpoitns are there
#   """
#   def uniquify(l):
#     c = itertools.count(start=1)
#     return [item.set_name(item.name+" "+str(c.next())) if isinstance(item,node.Node) else item+" "+str(c.next()) for item in l]

#   if isinstance(obj, node.Obj):
#     #check obj._nk.nodes to make sure everything from node_types is there
#     try:
#       required_points = node_types.get_required_points(obj.__class__.__name__)
#     except:
#       print "No list of required points for %s in node_types.type_dict['objects'][%s]" % (obj.__class__.__name__, obj.__class__.__name__)
#       required_points = None
#   elif isinstance(obj, node.Point):
#     #check obj.attributes
#     try:
#       required_points = node_types.get_required_points(obj.__class__.__name__)
#     except:
#       print "No list of required points for %s in node_types.type_dict['points'][%s]" % (obj.__class__.__name__, obj.__class__.__name__)
#       required_points = None
#   #now make sure that all points in required_points are in the points dict
#   objects = list(itertools.chain(*map(lambda x: uniquify(x) if isinstance(x,list) else [x],points.values())))
#   newkeys = list(itertools.chain(*map(lambda x: uniquify([x]*len(points[x])) if isinstance(points[x],list) else [x],points.keys())))
#   points = dict(zip(newkeys,objects))
#   if not required_points:
#     raise NotImplementedError
#   for reqpt in required_points:
#     if reqpt not in map(lambda x: x.split(' ')[0], points.keys()):
#       raise NotImplementedError(reqpt+" is not provided")
#   return points


class AHU(node.Obj):
  """
  Logic for Air Handlers
  """
  implements(interfaces.IAHU)

  required_setpoints = ['ZON_AIR_STP_CMD']
  required_devices = ['OUT_AIR_DMP', 'OUT_AIR_TMP_SEN', 'MIX_AIR_TMP_SEN', 'RET_FAN', 'RET_AIR_FLW_SEN',
                     'EXH_AIR_DMP', 'RET_AIR_HUM_SEN', 'RET_AIR_TMP_SEN', 'RET_AIR_DMP', 'RET_AIR_PRS_SEN',
                     'COO_VLV', 'SUP_AIR_FAN', 'SUP_AIR_FLW_SEN','SUP_AIR_TMP_SEN','SUP_AIR_PRS_SEN']

  def get_airflow():
    pass

  def set_airflow():
    pass

  def set_zone_temp():
    pass

class CWL(node.Obj):
  implements(interfaces.ICWL)

  required_setpoints =  ['CHL_WAT_PRS_DIF_STP']
  required_devices = ['CON_WAT_COO_TOW','CON_WAT_SUP_TMP_SEN','CON_WAT_PMP','CON_CHL_WAT_CHR',
                      'CON_WAT_RET_TMP_SEN','CHL_WAT_SUP_TMP_SEN','CHL_WAT_RET_TMP_SEN',
                      'CHL_WAT_PMP','CHL_WAT_PRS_DIF_SEN']

class HWL(node.Obj):
  implements(interfaces.IHWL)

  required_setpoints = ['HOT_WAT_RET_TMP_STP','HOT_WAT_PRS_DIF_STP','HOT_WAT_SUP_TMP_STP']
  required_devices = ['HX','HOT_WAT_RET_TMP_SEN','HOT_WAT_PRS_DIF_SEN','HOT_WAT_PMP','HOT_WAT_SUP_TMP_SEN']

class VAV(node.Obj):
  implements(interfaces.IVAV)

  required_devices = ['EXH_AIR_FAN']

class LIG(node.Obj):
  implements(interfaces.ILIG)

  required_setpoints = []
  required_devices = ['HI_REL','LO_REL']

  def get_relays(self):
    return self['HI_REL'], self['LO_REL']

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

""" 
Double checks to make sure all of the user-provided implementations correctly
implement the classes
"""
classes = [i[1] for i in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
ifaces = node_types.list_interfaces()
error = False
for i in ifaces:
  for cl in classes:
    if i.implementedBy(cl):
      if getValidationErrors(i,cl):
        error = True
        print cl.__name__,"does not correctly implement",i.__name__,getValidationErrors(i,cl)
if error:
  print "Something is wrong! Double-check your interface implementations"
  sys.exit(0)
