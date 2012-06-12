import uuid
import networkx as nx
import zope.interface

class Node(object):
  """
  Inherited class for nodes and objects (below)
  Uses uuid as a unique identifier, has optional name
  Supports methods add_child, add_parent
  """

  def __init__(self, container, name):
    """
    obj_type: string that conforms to the list of recognized object types
    container: Obj or Relational of which this object is a part
    name: string name of this object
    """
    self.name = name
    self.container = container
    self.uid = uuid.uuid4()
    self.metadata = {}

    self.container.add_nodes(self)

  def __str__(self):
    return self.name

  def __cmp__(self, other):
    # use self.uuid to compare to other objects
    return self.uid.__cmp__(other.uid)

  def __hash__(self):
    return hash(self.uid)

  def add_child(self, child):
    """
    Give this node a child w/n the context of it's container graph
    child: Point or Obj (which ever this object's type is)
    """
    self.container.add_node_child(self, child)

  def add_parent(self, parent):
    """
    Give this node a parent w/n the context of it's container graph
    parent: Point or Obj (which ever this object's type is)
    """
    self.container.add_node_parent(self, parent)

  @property
  def type(self):
    for interface in zope.interface.providedBy(self):
      if interface.__name__.startswith('I'):
        return interface.__name__[1:]
    return ''


class Container(object):
  """
  Inheritable class for handling basic graph operations beyond what networkx provides
  """
  def __init__(self, objects):
    self._nk = nx.DiGraph()
    if objects:
      for obj in objects:
        obj.container = self
        self._nk.add_node(obj)

  def draw_graph(self, filename="out.png")
    """
    Uses matplotlib.pyplot and nx.draw_circular to make a graph and saves it as "out.png"
    """
    import matplotlib.pyplot as plt
    nx.draw_circular(self._nk, fileanem)
    plt.show()

  def add_node_child(self, node, child):
    """
    check if child exists as a node in our interal graph
    if false, add the child then add the edge
    regardless, add edge if edge doesn't exist

    node,child: type Obj
    """
    if child not in self._nk:
      self._nk.add_node(child)
    if child not in self._nk[node]:
      self._nk.add_edge(node,child)

  #add parent to an internal node
  def add_node_parent(self, node, parent):
    """
    check if parent exists as a node in our interal graph
    if false, add the parent then add the edge
    regardless, add edge if edge doesn't exist

    node,parent: type Obj
    """
    if parent not in self._nk:
      self._nk.add_node(parent)
    if node not in self._nk[parent]:
      self._nk.add_edge(parent,node)

  #for internal graph setup
  def add_nodes(self, nodes):
    """
    Associates nodes with this object's internal graph
    """
    extension = [nodes] if type(nodes) != list else nodes
    for node in extension:
      node.container = self
      self._nk.add_node(node)

  def search(self, fn, retfn=lambda x: x):
    """
    searches dfs preorder for nodes for which the function [fn] evaluates to true
    It appends all True values to a results list, and applies [retfn] to them
    """
    results = []
    #apply fn to arbitrary node, make sure that it is a binary fxn
    tmp = self._nk.nodes()[0]
    if fn(tmp) not in [True, False]:
      print "Function must return True or False"
      return None
    for nd in nx.dfs_preorder_nodes(self._nk):
      if fn(nd):
        results.append(retfn(nd))
      #if the node is itself a container, we search it too!
      if hasattr(nd,"_nk"):
        results.extend(nd.search(fn,retfn))
    return results

class Point(Node):
  """
  Internal components of a larger object
  """

  def __init__(self, container, name):
    self.attributes = {}
    Node.__init__(self,container,name)
    print "Point",self.name, self.uid

  def set_attribute(self, att, value):
      self.attributes[att] = value

  def get_attribute(self, att):
      return self.attributes[att]

  def del_attribute(self, att):
      del self.attributes[att]

class Obj(Node, Container):

  def __init__(self, container, name, objects=[]):
    self.nodes = []
    Node.__init__(self, container, name)
    Container.__init__(self, objects)
    print ">>>Object",self.name, self.uid

class Relational(Container):

  def __init__(self, name, objects=[]):
    self.name = name
    Container.__init__(self, objects)

  #TODO: need this for queries?
  def extend_by_unique_uid(self, target, extend):
    extend = [extend] if type(extend) != list else extend
    to_add = [t for t in extend if t.uid not in map(lambda x: x.uid, target)]
    target.extend(to_add)

