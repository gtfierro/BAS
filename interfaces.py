import zope.interface

class IAH(zope.interface.Interface):
  """
  Interface for all Air Handler objects (type AH)

  For all objects that implement this, we probably want some sort of
  assert obj.type == "AH"
  """
  #high level methods will take form of:
  #def high_level_method(arg, arg, arg):
  # stuff
  # here
  # -> don't need to use "self" bc of how zope works
  pass

class ICWL(zope.interface.Interface):
  """
  Interface for all Chilled Water Loop objects (type CWL)
  """
  pass

class IHWL(zope.interface.Interface):
  """
  Interface for all Hot Water Loop objects (type HWL)
  """
  pass

class IFAN(zope.interface.Interface):
  """
  Interface for the FAN node
  """
  pass

class ICCV(zope.interface.Interface):
  """
  Interface for the CCV node
  """
  pass

class IDMP(zope.interface.Interface):
  """
  Interface for the DMP node
  """
  pass

class ISEN(zope.interface.Interface):
  """
  Interface for the SEN node
  """
  pass

class ICH(zope.interface.Interface):
  """
  Interface for the CH node
  """
  pass

class IHX(zope.interface.Interface):
  """
  Interface for the HX node
  """
  pass

class IPU(zope.interface.Interface):
  """
  Interface for the PU node
  """
  pass

class ICT(zope.interface.Interface):
  """
  Interface for the CT node
  """
  pass

class IVV(zope.interface.Interface):
  """
  Interface for the VV node
  """
  pass

