import sys
import node
import node_types
import inspect
import interfaces
from zope.interface import implements
from zope.schema import getValidationErrors

class BacNetAH(node.Obj):
  implements(node_types.get_interface('AH'))
  #TODO: replace 'actuation point' with the actual sMAP point

  _required_tags = {
                    'DIS_AIR_TMP_SEN'     : 'actuation point',
                    'DIS_AIR_FAN_SPD_CMD' : 'actuation point', 
                    'RET_AIR_FAN_SPD_CMD' : 'actuation point', 
                    'MIX_AIR_TMP_SEN'     : 'actuation point', 
                    'ZON_AIR_TMP_SEN'     : 'actuation point', 
                    'ZON_AIR_SPT_CMD'     : 'actuation point', 
                    'OUT_AIR_DMP_CMD'     : 'actuation point', 
                    'EXH_AIR_DMP_CMD'     : 'actuation point', 
                    }

  _optional_tags = {
                    'DIS_AIR_HUM_SEN'    : 'actuation point',
                    'DIS_AIR_PRS_SEN'    : 'actuation point',
                    'DIS_AIR_FLW_SEN'    : 'actuation point',
                    'DIS_AIR_FAN_POW_SEN'    : 'actuation point',
                    'RET_AIR_TMP_SEN'    : 'actuation point',
                    'RET_AIR_HUM_SEN'    : 'actuation point',
                    'RET_AIR_PRS_SEN'    : 'actuation point',
                    'RET_AIR_FLW_SEN'    : 'actuation point',
                    'RET_AIR_CO2_SEN'    : 'actuation point',
                    'RET_AIR_FAN_POW_SEN'    : 'actuation point',
                    'ZON_AIR_HUM_SEN'    : 'actuation point',
                    'ZON_AIR_CO2_SEN'    : 'actuation point',
                    'OUT_AIR_TMP_SEN'    : 'actuation point',
                    'OUT_AIR_HUM_SEN'    : 'actuation point',
                    'OUT_AIR_PRS_SEN'    : 'actuation point',
                    'OUT_AIR_FLW_SEN'    : 'actuation point',
                    'OUT_AIR_FLW_STP_CMD': 'actuation point',
                    'EXH_AIR_FAN_CMD'     : 'actuation point',
                  }

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

def validate():
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
  return not error

if not validate():
  sys.exit(0)
else:
  print "#"*64
  print "#"+" "*62+"#"
  print "# All interfaces implemented in bacnet_classes.py are verified #"
  print "#"+" "*62+"#"
  print "#"*64
