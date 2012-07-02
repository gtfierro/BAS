import node
import inspect
import object_types
import device_types
import generic_objects
import bacnet_devices
import zope.interface

abbreviations = {
    'DIS' : 'Discharge',
    'AIR' : 'Air',
    'TMP' : 'Temperature',
    'SEN' : 'Sensor',
    'SPD' : 'Speed',
    'CMD' : 'Point of Actuation',
    'RET' : 'Return',
    'MIX' : 'Mixed',
    'ZON' : 'Zone',
    'SPT' : 'Setpoint',
    'OUT' : 'Outside',
    'DMP' : 'Damper',
    'HUM' : 'Humidity',
    'PRS' : 'Pressure',
    'FLW' : 'Flow',
    'POW' : 'Power',
    'CO2' : 'Carbon Dioxide',
    'EXH' : 'Exhaust',
    'FAN' : 'Fan',
    'COO' : 'Cooling',
    'VLV' : 'Valve',
    'AHU' : 'Air Handler',
    'CCV' : 'Cooling Coil',
    'CWL' : 'Cold Water Loop',
    'HWL' : 'Hot Water Loop',
    'REL' : 'Relay',
    'HI'  : 'High',
    'LO'  : 'Low',
    'LIG' : 'Light',
    }

def list_objects():
  return [v for v in vars(generic_objects).values() if type(v) == type and issubclass(v, node.Obj)]

def list_devices():
  return [v for v in vars(bacnet_devices).values() if type(v) == type and issubclass(v, node.Device)]

def list_tags(targ=''):
  """ Returns a list of all tags"""
  tags = set()
  for cls in list_objects():
    if targ and not cls.type() == targ:
        continue
    tags |= set(cls.required_devices)
  for driver in list_devices():
    if targ and not driver.type() == targ:
        continue
    tags |= set(driver.required_points)
  return list(tags)

def list_types():
  """ Returns a list of all types"""
  types = []
  types.extend(x.type() for x in list_objects())
  types.extend(x.type() for x in list_devices())
  return types

def get_tag_name(tag):
  """ convert something like DIS_AIR_TMP_SEN to Discharge Air Temp Sensor """
  #convert tag to a list
  tag = tag.split("_") if "_" in tag else [tag]
  classification = [abbreviations[prefix] for prefix in tag if prefix in abbreviations ]
  return " ".join(classification)

def get_required_setpoints(s):
  """ Return list of required setpoints for a given string e.g. 'AH' """
  if s in vars(generic_objects):
    return getattr(generic_objects, s).required_setpoints
  else:
    return getattr(bacnet_devices, s).required_setpoints

def get_required_points(s):
  """ Return list of required points for a given string e.g. 'AH' """
  if s in vars(generic_objects):
      return getattr(generic_objects, s).required_devices
  else:
    return getattr(bacnet_devices, s).required_points

def verify_list(l):
  for el in l:
    for i in zope.interface.implementedBy(el):
      zope.interface.verify.verifyClass(i, el)

def verify_devices():
  return verify_list(list_devices())

def verify_objects():
  return verify_list(list_objects())

def get_class(target):
  """
  returns the class in generic_objects that [target] inherits from
  """
  classes = map(lambda x: x[1], inspect.getmembers(generic_objects,predicate=inspect.isclass))
  target_class = filter(lambda x: isinstance(target, x), classes)
  return target_class[0] if target_class else None

def get_methods(target):
  """
  Returns a list of non-inherited methods for [target], which can be either a device
  or an object for the purposes of the API
  """
  base_attributes = filter(lambda x: not x[0].startswith("_"), get_class(target).__dict__.keys())
  methods = filter(lambda x: inspect.ismethod(getattr(target, x)), base_attributes)
  ret = {}
  for m in methods:
    ret[m] = inspect.getdoc(getattr(target,m))
  return ret
