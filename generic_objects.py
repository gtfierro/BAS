"""
Contains the pre-implemented logic for the higher level objects like the AHU, HWL, CWL.
Each of these classes should be initialized with the specific instantiations of drivers that
they expect in order to provide the full functionality of the class. The drivers they expect can 
be found in node_types.get_required_setpoints('AHU'), node_types.get_required_devices('AHU'), etc
"""
import node
import object_types
from zope.interface import implements

class AHU(node.Obj):
  """
  Logic for Air Handlers
  """
  implements(object_types.IAHU)

  required_setpoints = ['ZON_AIR_STP_CMD']
  required_devices = ['OUT_AIR_DMP', 'OUT_AIR_TMP_SEN', 'MIX_AIR_TMP_SEN', 'RET_FAN', 'RET_AIR_FLW_SEN',
                     'EXH_AIR_DMP', 'RET_AIR_HUM_SEN', 'RET_AIR_TMP_SEN', 'RET_AIR_DMP', 'RET_AIR_PRS_SEN',
                     'COO_VLV', 'SUP_AIR_FAN', 'SUP_AIR_FLW_SEN','SUP_AIR_TMP_SEN','SUP_AIR_PRS_SEN']

  def get_airflow(self):
    pass

  def set_airflow(self, airflow):
    pass

  def set_zone_temp(self):
    pass

class CWL(node.Obj):
  implements(object_types.ICWL)

  required_setpoints =  ['CHL_WAT_PRS_DIF_STP']
  required_devices = ['CON_WAT_COO_TOW','CON_WAT_SUP_TMP_SEN','CON_WAT_PMP','CON_CHL_WAT_CHR',
                      'CON_WAT_RET_TMP_SEN','CHL_WAT_SUP_TMP_SEN','CHL_WAT_RET_TMP_SEN',
                      'CHL_WAT_PMP','CHL_WAT_PRS_DIF_SEN']

class HWL(node.Obj):
  implements(object_types.IHWL)

  required_setpoints = ['HOT_WAT_RET_TMP_STP','HOT_WAT_PRS_DIF_STP','HOT_WAT_SUP_TMP_STP']
  required_devices = ['HX','HOT_WAT_RET_TMP_SEN','HOT_WAT_PRS_DIF_SEN','HOT_WAT_PMP','HOT_WAT_SUP_TMP_SEN']

class VAV(node.Obj):
  implements(object_types.IVAV)

  required_devices = ['EXH_AIR_FAN']

class LIG(node.Obj):
  implements(object_types.ILIG)

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

