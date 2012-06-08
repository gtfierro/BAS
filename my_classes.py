from bacnet_classes import *
import interfaces
import btypes
from zope.interface import implements


class MyAirHandler(BObj):
  implements(btypes.type_dict['AH']['interface'])
   
