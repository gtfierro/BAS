from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Dict, Choice
from zope.schema import getValidationErrors

class DREL(Interface):
  """
  Driver for the Relay nodes
  """
  def get_brightness():
    """Get brightness level"""
  def set_brightness(value):
    """set brightness to value"""

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

class DCHR(Interface):
  """
 Driver for the CH node
  """
  pass

class DHX(Interface):
  """
 Driver for the HX node
  """
  pass

class DPMP(Interface):
  """
 Driver for the PMP node
  """
  pass

class DTOW(Interface):
  """
 Driver for the TOW node
  """
  pass

class DVLV(Interface):
  """
 Driver for the VLV node
  """
  pass

