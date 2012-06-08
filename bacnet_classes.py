import uuid
import sys
import re
import btypes
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from collections import defaultdict
from zope.interface import implements
from interfaces import *

class BACnetPoint(object):
  """
  Inherited class for nodes and objects (below)
  Uses uuid as a unique identifier, has optional name
  Supports methods add_child, add_parent
  """
  implements(BACnetInterface)

  def __init__(self, obj_type, container='', name=''):
    """
    obj_type: string that conforms to the list of recognized object types
    container: BObj or Relational of which this object is a part
    name: string name of this object
    """
    self.type = obj_type
    self.name = name
    self.container = container
    self.uid = uuid.uuid4()
    self.metadata = {}

  def __str__(self):
    return self.name

  def __cmp__(self, other):
    # use self.uuid to compare to other objects
    return self.uid.__cmp__(other.uid)

  def add_child(self, child):
    """
    Give this node a child w/n the context of it's container graph
    child: BNode or BObj (which ever this object's type is)
    """
    self.container.add_node_child(self, child)

  def add_parent(self, parent):
    """
    Give this node a parent w/n the context of it's container graph
    parent: BNode or BObj (which ever this object's type is)
    """
    self.container.add_node_parent(self, parent)

class Container(object):
  """
  Inheritable class for handling basic graph operations beyond what networkx provides
  """
  def __init__(self, objects):
    self._nk = nx.DiGraph()
    self.type_dict = defaultdict(list)
    if objects:
      for obj in objects:
        obj.container = self
        self._nk.add_node(obj)
    self._populate_type_dict()

  def _populate_type_dict(self):
    for o in self._nk.nodes():
      if o not in self.type_dict[o.type]:
        self.type_dict[o.type].append(o)
      #will only iterate through nodes if the objects we iterated through
      #above also inherit from Container
      if "Container" in [par.name for par in o.__class__.__bases__]:
        for n in o._nk.nodes():
          if n not in self.type_dict[n.type]:
            self.type_dict[n.type].append(n)

  def add_node_child(self, node, child):
    """
    check if child exists as a node in our interal graph
    if false, add the child then add the edge
    regardless, add edge if edge doesn't exist

    node,child: type BObj
    """
    if child not in self._nk:
      self._nk.add_node(child)
    if child not in self._nk[node]:
      self._nk.add_edge(node,child)
    self._populate_type_dict()

  #add parent to an internal node
  def add_node_parent(self, node, parent):
    """
    check if parent exists as a node in our interal graph
    if false, add the parent then add the edge
    regardless, add edge if edge doesn't exist

    node,parent: type BObj
    """
    if parent not in self._nk:
      self._nk.add_node(parent)
    if node not in self._nk[parent]:
      self._nk.add_edge(parent,node)
    self._populate_type_dict()

  #for internal graph setup
  def add_nodes(self, nodes):
    """
    Associates nodes with this object's internal graph
    """
    extension = [nodes] if type(nodes) != list else nodes
    for node in extension:
      node.container = self
      self._nk.add_node(node)


class BNode(BACnetPoint):
  """
  Internal components of a larget object  
  """

  def __init__(self, obj_type, container, name):
    self.attributes = {}
    BACnetPoint.__init__(self,obj_type,container,name)
    print "Node",self.name, self.uid
  
class BObj(BACnetPoint,Container):

  def __init__(self, obj_type, container, name):
    self.nodes = []
    self._nk = nx.DiGraph()
    self.type_dict = defaultdict(list)
    BACnetPoint.__init__(self,obj_type, container, name)
    print ">>>Object",self.name, self.uid

class Relational(Container):

  def __init__(self, name, objects=None):
    self._nk = nx.DiGraph()
    self.type_dict = defaultdict(list)
    self.name = name
    if objects:
      for obj in objects:
        obj.container = self
        self._nk.add_node(obj)
    self._populate_type_dict()

  #TODO: need this for queries?
  def extend_by_unique_uid(self, target, extend):
    extend = [extend] if type(extend) != list else extend
    to_add = [t for t in extend if t.uid not in map(lambda x: x.uid, target)]
    target.extend(to_add)

