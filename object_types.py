from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Dict, Choice
from zope.schema import getValidationErrors

class IAHU(Interface):
  """
  Interface for all Air Handler objects (type AHU)
  """

  def set_airflow(airflow):
    """sets the airflow to all derivative VAVs for this Air Handler to be [airflow]"""

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

class IVAV(Interface):
  """
  Interface for the Variable Air Volume boxes
  """
  def get_airflow():
    """get airflow of the VAV"""

  def set_airflow(airflow):
    """set the airflow setpoint for the VAV to be [airflow]"""

class ILIG(Interface):
  """
  Interface for all the lightbanks
  """

  def get_level():
    """get the level of the lightbank"""

  def set_level(level):
    """set the level of the lightbank"""

