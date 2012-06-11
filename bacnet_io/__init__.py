import sys
import bacnet
from bacnet import *
import os
import time
import cPickle as pickle
import operator
import types

class BacnetBase:
  ''' Abstract class providing user-friendly read and write routines '''

  def read_point(self, prop = bacnet.PROP_PRESENT_VALUE, array_index = -1, full = False):
    ret = self._read(prop, array_index)
    # TODO: destinguish between a None reply (e.g. read_point(('WS86001', 'RELAY05'), PROP_UNITS))
    # and a reading error/timeout.
    if ret == None or len(ret) == 0:
      return None
    else:
      if len(ret) > 1:
        return ret
        #raise Exception('Unexpected')
      ret = ret[0]
      if type(ret) is types.TupleType and not full:
        return ret[0]
      else:
        return ret

  def write_point(self, type, value, priority = 16):
    # Retry the write if we have an error
    for retry_sleep in [0, 1, 5, 30]:
      time.sleep(retry_sleep)
      if self._write(type, value, priority) == 1:
        return
    raise Exception('Error writing: ' + str(self))
   
  def clear_point(self, priority = 16):
    return self.write_point(bacnet.BACNET_APPLICATION_TAG_NULL, 1, priority)

class BacnetDev(BacnetBase):
  def __init__(self, h_dev):
    self.h_dev = h_dev
    self.name = self.read_point(bacnet.PROP_OBJECT_NAME)
    if self.name == None:
      raise Exception('Device has no name: ' + str(self))
    self.desc = self.read_point(bacnet.PROP_DESCRIPTION)
    self.objs = []

  def _add_obj(self, obj):
    self.objs.append(obj)

  def _read(self, prop, array_index = -1):
    return bacnet.read_prop(self.h_dev, bacnet.OBJECT_DEVICE,
        self.h_dev['device_id'], prop, array_index)

  def __str__(self):
    return '%s (%d)' % (self.name, self.h_dev['device_id'])

class BacnetObj(BacnetBase):
  def  __init__(self, h_obj, parent):
    self.h_obj = h_obj
    self.parent = parent

    self.name = self.read_point(bacnet.PROP_OBJECT_NAME)
    if self.name == None:
      raise Exception('Device has no name: ' + str(self))
    self.desc = self.read_point(bacnet.PROP_DESCRIPTION)
    self.units = self.read_point(bacnet.PROP_UNITS, full = True)

  def get_type(self):
    return self.h_obj['type']

  def get_parent_name(self):
    return self.parent.name if self.parent else None

  def _read(self, prop, array_index = -1):
    return bacnet.read_prop(self.parent.h_dev, self.h_obj['type'],
        self.h_obj['instance'], prop, array_index)

  def _write(self, type, value, priority = 16):
    return bacnet.write_prop(
        self.parent.h_dev,
        self.h_obj['type'],
        self.h_obj['instance'],
        bacnet.PROP_PRESENT_VALUE,
        type,
        str(value).strip(),
        int(priority))

  def __str__(self):
    return '%s (t: %d, i: %d)' % (self.name, self.h_obj['type'], self.h_obj['instance'])

class BacnetIO:
  ''' User-friendly class for finding and listing bacnet points '''

  def __init__(self, db_file, nic = None, port = None):
    def _find_db():
      for d in [sys.prefix, os.path.dirname(__file__)]:
        filename = os.path.join(d, db_file)
        if os.path.exists(filename):
          return filename
      raise Exception("Database file not found: " + filename)
  
    self.dev_list = pickle.load(open(_find_db(), 'rb')) 
    bacnet.Init(nic, str(port))

  def clear_point(self, obj_name, priority = 16):
    o = self.find(obj_name)
    if o == None:
      raise Exception('Point %s not found.' % obj_name)
    return o.clear_point(priority)

  def write_point(self, obj_name, type, value, priority = 16):
    o = self.find(obj_name)
    if o == None:
      raise Exception('Point %s not found.' % obj_name)
    return o.write_point(type, value, priority)

  def read_point(self, obj_name, prop = bacnet.PROP_PRESENT_VALUE, array_index = -1, full = False):
    o = self.find(obj_name)
    if o == None:
      raise Exception('Point %s not found.' % obj_name)
    return o.read_point(prop, array_index, full)

  def find(self, obj_name, dev_name = None, prefix = False):
    def matches(a,b):
      if prefix:
        return b.lower().startswith(a.lower())
      else:
        return b.lower() == a.lower()

    for dev in self.dev_list:
      if not dev_name or matches(dev_name, dev.name):
        for obj in dev.objs:
          if matches(obj_name, obj.name):
            return obj
    return None
  
  def search(self, string, case_sensitive=False):
    """
    Searches for [string] in the names of all devices/objects in this bacnet_io object
    """
    for dev in self.dev_list:
      for obj in dev.objs:
        if string in (obj.name if case_sensitive else obj.name.lower()):
          print dev.name, obj.name, dev.objs.index(obj)

  @staticmethod
  def _sorter(list, sort):
    if sort:
      return sorted(list, key=operator.attrgetter('name'))
    else:
      return list

  def list_dev(self, sort = False):
    return self._sorter(self.dev_list, sort)
    
  def list(self, sort = False):
    for dev in self._sorter(self.dev_list, sort):
      for obj in self._sorter(dev.objs, sort):
        yield obj
