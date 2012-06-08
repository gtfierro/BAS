import node
import types
from zope.interface import implements

class MyAirHandler(node.Obj):
  implements(types.get_interface('AH'))
