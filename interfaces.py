import zope.interface


class BACnetInterface(zope.interface.Interface):
  """
  Interface that all objects/nodes must implement
  """
  
  type = interface.Attribute("allowed 2-3 char A-Z string from btypes.py")
  name = interface.Attribute("string name, not necessarily unique")
  container = interface.Attribute("reference to the containing BObj or Relational object")
  uid = interface.Attribute("UUID")

  def add_child(child):
    """
    Give this node a child w/n the context of it's container graph
    child: BNode or BObj (which ever this object's type is)
    """

  def add_parent(parent):
    """
    Give this node a parent w/n the context of it's container graph
    parent: BNode or BObj (which ever this object's type is)
    """

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

