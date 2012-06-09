import node
import node_types
from zope.interface import implements

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
