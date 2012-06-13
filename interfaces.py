from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Dict, Choice
from zope.schema import getValidationErrors
from node_types import *

#TODO: do what I did for IAH for all other interfaces, both here, in tags.txt and in node_types.py

class IAH(Interface):
  """
  Interface for all Air Handler objects (type AH)

  All Air Handlers must have 2 dictionaries, _required_tags and _optional_tags with keys
  that are the abbreviated tag names listed in node_types.type_dict and values that correspond
  to the smap lookup/actuation points for those tags
  """
  _required_tags = Dict(
                    title = u'Required Tags for Air Handler',
                    required=True,
                    min_length = len(get_required_tags('AH')),
                    max_length = len(get_required_tags('AH')),
                    key_type = Choice(values = tuple(get_required_tags('AH')))
                   )

  _optional_tags = Dict(
                    title = u'Optional Tags for Air Handler',
                    required=True,
                    key_type = Choice(values = tuple(get_optional_tags('AH')))
                   )

  #high level methods will take form of:
  #def high_level_method(arg, arg, arg):
  # stuff
  # here
  # -> don't need to use "self" bc of how zope works

class ICWL(Interface):
  """
  Interface for all Chilled Water Loop objects (type CWL)
  """
  pass

class IHWL(Interface):
  """
  Interface for all Hot Water Loop objects (type HWL)
  """
  pass

class IFAN(Interface):
  """
  Interface for the FAN node
  """
  pass

class ICCV(Interface):
  """
  Interface for the CCV node
  """
  pass

class IDMP(Interface):
  """
  Interface for the DMP node
  """
  pass

class ISEN(Interface):
  """
  Interface for the SEN node
  """
  pass

class ICH(Interface):
  """
  Interface for the CH node
  """
  pass

class IHX(Interface):
  """
  Interface for the HX node
  """
  pass

class IPU(Interface):
  """
  Interface for the PU node
  """
  pass

class ICT(Interface):
  """
  Interface for the CT node
  """
  pass

class IVV(Interface):
  """
  Interface for the VV node
  """
  pass

