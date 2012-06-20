from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Dict, Choice
from zope.schema import getValidationErrors
from node_types import *

class DREL(Interface):
  """
  Driver for the Relay nodes
  """
  def turn_on():
    """Turn this light relay on"""

  def turn_off():
    """Turn this light relay off"""

  def get_level():
    """Get current level of the relay"""

class DFAN(Interface):
  """
 Driver for the FAN node
  """
  pass

class DCCV(Interface):
  """
 Driver for the CCV node
  """
  pass

class DDMP(Interface):
  """
 Driver for the DMP node
  """
  pass

class DSEN(Interface):
  """
 Driver for the SEN node
  """
  pass

class DCH(Interface):
  """
 Driver for the CH node
  """
  pass

class DHX(Interface):
  """
 Driver for the HX node
  """
  pass

class DPU(Interface):
  """
 Driver for the PU node
  """
  pass

class DCT(Interface):
  """
 Driver for the CT node
  """
  pass

class DVV(Interface):
  """
 Driver for the VV node
  """
  pass

