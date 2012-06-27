import sys
import code
import inspect
import test
import itertools
import networkx as nx
from ply.lex import lex
from ply.yacc import yacc
from node import *
from node_types import *
from collections import deque
import gis

class Lexer(object):

  tokens = [
      'NAME','TYPE','UUID','VAR','TAG','SPATIAL',
      'UPSTREAM','DOWNSTREAM','EQUALS','KEYWORD','LASTVALUE',
      'LPAREN','RPAREN',
      ]

  #Tokens

  t_UPSTREAM    = r'>' 
  t_DOWNSTREAM  = r'<'
  t_LPAREN      = r'\('
  t_RPAREN      = r'\)'
  t_EQUALS      = r'='
  t_ignore      = ' \t'

  def t_NAME(self,t):
    r'\$[\w\-\:\_\s]+'
    t.value = t.value.strip()
    return t

  def t_SPATIAL(self,t):
    r'!!?[\w\-\:\_\s]+'
    t.value = t.value.strip()
    return t

  def t_TYPE(self,t):
    r'\#!?[A-Z0-9]+[ ]?'
    t.value = t.value.strip()
    return t
 
  def t_UUID(self,t):
    r'\%!?[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}[ ]?'
    t.value = t.value.strip()
    return t

  def t_VAR(self,t):
    r'\@[a-zA-Z_][a-zA-Z0-9_]*[ ]?'
    t.value = t.value.strip()
    return t

  def t_TAG(self,t):
    r'\&!?[A-Z_]+[ ]?'
    t.value = t.value.strip()
    return t

  def t_LASTVALUE(self,t):
    r'\b\_\b'
    t.value = t.value.strip()
    return t

  def t_KEYWORD(self, t):
    r'\b(help|types|prefixes|examples|tags|actuate)\b'
    if t.value == 'help':
      print " help: returns this help list \n types: returns list of types you can query \n tags: returns a list of tags you can query \n prefixes: returns list of prefixes for queries \n examples: lists some example queries"
    elif t.value == 'types':
      print list_types()
    elif t.value == 'tags':
      print list_tags()
    elif t.value == 'prefixes':
      print " #TYPE: designates set of all objects with type [TYPE] \n $Name Of Object: designates set of all objects named [Name of Object] (case sensitive \n %ab61b939-a133-4d76-b9c4-a5d6fab7abf5: designates object tagged with uuid \n @var_name: you can assign queries to variables and use them in later queries \n &TAG designates set of all objects tagged as TAG"
    elif t.value == 'examples':
      print " #DMP < $Return Air Handler: give me all dampers downstream of the Return Air Handler"
    elif t.value == 'actuate':
      return t
    t.lexer.skip(1)

  def t_error(self,t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

class Parser(object):

  def __init__(self,debug_flag=False):
    self.debug = debug_flag
    self.lexer = lex(module=Lexer())
    self.relationals = [getattr(test, i) for i in test.__dict__ if isinstance(getattr(test,i), Relational)]
    self.domain = []
    self.vars = {}
    self.lastvalue = []

  def call_actuation_console(self):
    """
    Start an interactive python console with the local variables and names preloaded 
    into the environment
    """
    local_vars = {}
    for k in self.vars.iterkeys():
      local_vars[k[1:]] = self.vars[k]
    try:
      from IPython.frontend.terminal.embed import TerminalInteractiveShell
      from IPython.frontend.terminal.ipapp import load_default_config
      config = load_default_config()
      shell = TerminalInteractiveShell(config=config, user_ns=local_vars)
      shell.mainloop()
    except ImportError:
      console = code.InteractiveConsole(local_vars)
      console.interact()


  def _links_to_nodes(self, links):
    for r in self.relationals:
      for node in r.nodes:
        if str(node.uid) in [link.uuid for link in links]:
            yield node

  def links_to_nodes(self, links):
      return Node.NodeList(self._links_to_nodes(links))

  def get_areas(self, gisobj):
    """
    returns a list of the areas for the given gisobj
    """
    areas = [gisobj] if not isinstance(gisobj,list) else gisobj
    flattened = []
    for place in areas:
      if isinstance(place, gis.Building):
        for floor in place.floors.all():
          flattened.extend(list(floor.areas.all()))
      if isinstance(place, gis.Floor):
        flattened.extend(list(place.areas.all()))
      else:
        flattened.append(place)
    return flattened

  def areas_to_nodes(self, areas):
    """
    For every item in [areas], we resolve it down to all areas inside it and
    then return the flat list of all nodes in those areas
    """
    areas = self.get_areas(areas)
    return self.links_to_nodes(list(itertools.chain.from_iterable(x.nodes.all() for x in areas)))
  
  def nodes_to_areas(self,nodes):
    nodes = [nodes] if not isinstance(nodes,list) else nodes
    flattened = []
    for node in nodes:
      extension = node.areas.all()
      if extension:
        flattened.extend(extension) 
    return flattened

  def filter_dup_uids(self, target):
    """
    Given a [target] list, returns a list where all components are unique by their uid
    """
    ret = []
    for item in target:
      if hasattr(item,'uid'):
        if item.uid not in map(lambda x: x.uid, ret):
          ret.append(item)
      else: #if it doesn't have a uid, then it's a spatial
        ret.append(item)
    return ret

  def search_relatives(self, node, target, direction):
    """
    [direction] is either "successors" or "predecessors"
    Given a [node], search all of its successors: Successors are all nodes reachable by a bfs from this node
    as well as the container of this node (if it exists) and all successors of that object and all nodes 
    in those successors. As soon as we find a successor that is in [target], we return [node], but if we reach
    the end of the recursion, then we return None.

    How do we do this? We can get the immediate successors for a node using node.container._nk.successors(node)
    put these all onto a deque, followed by the container. We iterate through this generator, checking for membership in [target]. As we pop 
    nodes off the deque, we add their immediate children to the deque.
    """
    #initialize whether we're looking for successors or predecessors
    relative_fxn = lambda x: getattr(x.container._nk, direction)(x)
    #initialize already-visited lists
    already_visited = [node]
    #initialize queue
    queue = deque()
    #add first node to queue
    queue.appendleft(node)
    #add its Container if it isn't already a container
    if not isinstance(node, Container):
      queue.appendleft(node.container)
      already_visited.append(node.container)

    while queue: #loop until we reach the end of the queue
      #get next node off the top (FIFO)
      current = queue.pop()
      if current in target: #successful!
        return node
      #if this node is in a container we haven't visited yet, add
      #all of that container's nodes to our queue
      if isinstance(current, Container):
        if current not in already_visited:
          for n in current._nk.nodes():
            if n not in already_visited:
              already_visited.append(n)
              queue.appendleft(n)
      #search the relatives of the current node according to relative_fxn
      #for each relative, if we haven't traversed it, add it to the queue
      for n in relative_fxn(current):
        if n not in already_visited:
          already_visited.append(n)
          queue.appendleft(n)
      #if current has an external container, add it to the queue
      if current.external_parents and direction == "predecessors":
        for p in current.external_parents:
          if p not in already_visited:
            queue.appendleft(p)
      elif current.external_childs and direction == "successors":
        for c in current.external_childs:
          if c not in already_visited:
            queue.appendleft(c)
      #finally, add the current's container to the queue
      if not isinstance(current.container, Relational):
        if current.container not in queue and current.container not in already_visited:
          already_visited.append(current.container)
          queue.appendleft(current.container)
    return None

  def isspatial(self, nodes):
    """
    returns True if [nodes] contains spatial objects
    """
    nodes = [nodes] if not isinstance(nodes,list) else nodes
    return all(map(lambda x: not isinstance(x, (Relational, Node)),nodes))

  def resolve_spatial(self,node,target,direction):
    """
    resolve queries before we send them along to be resolved so that we're dealing with a constant datatype: spatials or objects

    1:spatial, 3:spatial => 'normal' spatial lookup, looking for some overlap between 1 and 3
    1:object, 3:spatial => resolve 3 to nodes, use the search_relatives fxn to filter 1
    1:spatial, 3:object => use nodes.areas and then go to the first case. go up the hierarchy
                            to find 3's areas
    1:object, 3:object => use search_relatives (just return node and target unchanged)
    """
    nodespatial = self.isspatial(node)
    targetspatial = self.isspatial(target)
    if targetspatial and not nodespatial: #resolve target into objects!
      target = self.areas_to_nodes(target)
      return node,target
    elif nodespatial and not targetspatial: #resolve target into areas!
      target = self.nodes_to_areas(target)
      targetspatial = True
    if nodespatial and targetspatial: #resolve the derivative relationship spatially
      target_regions = []
      node_regions = []
      #TODO: fix the filter stuff, decide what >,< mean
      for area in self.get_areas(target):
        target_regions.extend(gis.Area.objects.filter(regions__exact=area.regions))
      for area in self.get_areas(node):
        node_regions.extend(gis.Area.objects.filter(regions__exact=area.regions))
      return filter(lambda x: x in target_regions, node_regions), None
    else: #neither node nor target is spatial, so we do nothing
      return node,target

  def p_actuation(self,p):
    '''statement : KEYWORD'''
    if p[1] == 'actuate':
      self.call_actuation_console()

  def p_statement_assign(self,p):
    '''statement : VAR EQUALS query'''
    self.vars[p[1]] = p[3]

  def p_statement_query(self,p):
    '''statement : query'''
    self.lastvalue=p[1]
    p[0] = p[1]

  def p_query(self,p):
    '''query : query UPSTREAM set
             | query DOWNSTREAM set'''
    res = []
    domain,target = self.resolve_spatial(p[1],p[3],p[2])
    if not self.isspatial(domain) and not self.isspatial(target):
      if p[2] == ">": #upstream
        next_domain = [self.search_relatives(node, target,"successors") for node in domain]
      else:
        next_domain = [self.search_relatives(node, target,"predecessors") for node in domain]
      next_domain = filter(lambda x: x, next_domain)
      p[0] = self.lastvalue=self.filter_dup_uids(next_domain)
    else:
      p[0] = self.lastvalue=domain

  def p_query_set(self,p):
    '''query : set'''
    p[0] = self.lastvalue = self.filter_dup_uids(p[1])


  def p_set_group(self, p):
    '''set : LPAREN query RPAREN'''
    p[0] = self.lastvalue = p[2]

  def p_set_lastvalue(self,p):
    '''set : LASTVALUE'''
    p[0] = self.lastvalue

  def p_set_spatial(self, p):
    '''set : SPATIAL'''
    name_lookup = p[1][1:].strip()
    strict = False
    if name_lookup.startswith('!'):
      name_lookup = name_lookup[1:]
      strict = True
    p[0] = self.lastvalue = gis.search(name_lookup, strict)

  def p_set_name(self,p):
    'set : NAME'
    name_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in domain:
      res.extend(r.search(lambda x: x.name == name_lookup))
    p[0] = self.lastvalue = self.filter_dup_uids(res)

  def p_set_type(self,p):
    'set : TYPE'
    type_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in domain:
      res.extend(r.search(lambda x: x.type() == type_lookup))
    p[0] = self.lastvalue = self.filter_dup_uids(res)

  def p_set_uuid(self,p):
    'set : UUID'
    uuid_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in domain:
      res.extend(r.search(lambda x: str(x.uid) == uuid_lookup))
    p[0] = self.lastvalue = res

  def p_set_var(self,p):
    'set : VAR'
    p[0] = self.vars.get(p[1],[])

  def p_set_tag(self,p):
    'set : TAG'
    tag_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    domain = [r._nk.nodes() if isinstance(r,Relational) else r for r in domain]
    domain = list(itertools.chain(*domain))
    res = []
    for d in domain:
      if d[tag_lookup]:
        res.append(d[tag_lookup]) 
    p[0] = self.lastvalue = res

  def p_error(self,p):
    if p:
      print "Syntax error!",p

  tokens = Lexer.tokens


if __name__ == '__main__':
  debug= int(sys.argv[1]) if len(sys.argv) > 1 else 0
  lexer = lex(module=Lexer())
  parser = yacc(module=Parser(debug_flag=debug), write_tables=0)
  print "type 'help' for assistance"
  while True:
    query = raw_input("query> ")
    if not query:
      continue
    result = parser.parse(query)
    if result:
      for res in result:
        if isinstance(res, (Relational,Obj,Device)):
          print res.name,res.uid
        else: #it's a building!
          area = res.name.split(':')[-1] if isinstance(res, gis.Area) else ''
          floor = res if isinstance(res,gis.Floor) else res.floor if hasattr(res,'floor') else area.building if area else ''
          building = res if isinstance(res, gis.Building) else res.building if hasattr(res,'building') else floor.building if floor else ''
          print building,':',floor,':',area

def query(string):
  """returns list of objects as returned by the query language"""
  lexer = lex(module=Lexer())
  parser = yacc(module=Parser())
  return parser.parse(string)
