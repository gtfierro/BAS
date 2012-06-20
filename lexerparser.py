import sys
import test
import inspect
import networkx as nx
from ply.lex import lex
from ply.yacc import yacc
from node import *
from node_types import *
from collections import deque

class Lexer(object):

  tokens = [
      'NAME','TYPE','UUID','VAR',
      'UPSTREAM','DOWNSTREAM','EQUALS',
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
    # find everything with name t.value and replace t.value with that value
    t.value = t.value.strip()
    return t

  def t_TYPE(self,t):
    r'\#[A-Z0-9]+[ ]?'
    t.value = t.value.strip()
    return t
 
  def t_UUID(self,t):
    r'\%[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}[ ]?'
    t.value = t.value.strip()
    return t

  def t_VAR(self,t):
    r'\@[a-zA-Z_][a-zA-Z0-9_]*[ ]?'
    t.value = t.value.strip()
    return t

  def t_keyword(self, t):
    r'\b(help|types|prefixes|examples)\b'
    if t.value == 'help':
      print " help: returns this help list \n types: returns list of types you can query \n prefixes: returns list of prefixes for queries \n examples: lists some example queries"
    elif t.value == 'types':
      print list_types()
    elif t.value == 'prefixes':
      print " #TYPE: designates set of all objects with type [TYPE] \n $Name Of Object: designates set of all objects named [Name of Object] (case sensitive \n %ab61b939-a133-4d76-b9c4-a5d6fab7abf5: designates object tagged with uuid \n @var_name: you can assign queries to variables and use them in later queries"
    elif t.value == 'examples':
      print " #DMP < $Return Air Handler: give me all dampers downstream of the Return Air Handler"
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

  def filter_dup_uids(self, target):
    """
    Given a [target] list, returns a list where all components are unique by their uid
    """
    ret = []
    for item in target:
      if item.uid not in map(lambda x: x.uid, ret):
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
    relative_fxn = lambda x: getattr(x.container._nk, direction)(x)

    if self.debug: print "Starting Search: node:",node,"target:",[i.name for i in target]
    if self.debug: print "-"*20
    queue = deque()
    queue.appendleft(node)
    if not isinstance(node, Container):
      queue.appendleft(node.container) 
    already_visited_containers = [node.container]
    while queue:
      if self.debug: print "QUEUE:",[i.name for i in queue]
      current = queue.pop()
      if current in target: 
        if self.debug: print "returning",node
        if self.debug: print "+"*20
        return node
      if isinstance(current, Container):
        if current not in already_visited_containers:
          if self.debug: print "adding nodes in",current.name
          for n in current._nk.nodes():
            queue.appendleft(n)
      for n in relative_fxn(current):
        if self.debug: print "adding node",n.name
        queue.appendleft(n)
      if not isinstance(current.container, Relational):
        if current.container not in queue and current.container not in already_visited_containers:
          if self.debug: print "adding",current.name,"'s container",current.container.name
          already_visited_containers.append(current.container)
          queue.appendleft(current.container)
    if self.debug: print "*"*20
    return None

  def p_statement_assign(self,p):
    '''statement : VAR EQUALS query'''
    self.vars[p[1]] = p[3]

  def p_statement_query(self,p):
    '''statement : query'''
    p[0] = p[1]

  def p_query(self,p):
    '''query : query UPSTREAM set
             | query DOWNSTREAM set'''
    res = []
    if p[2] == ">": #upstream
      #we want all of the items in p[1] whose successors are in p[3]
      #res.extend(filter(lambda node: set([item for sublist in nx.dfs_successors(node.container._nk.node).values()]).intersection(set(p[3])),p[1]))
      next_domain = [self.search_relatives(node, p[3],"successors") for node in p[1]]
    else:
      next_domain = [self.search_relatives(node, p[3],"predecessors") for node in p[1]]
    next_domain = filter(lambda x: x, next_domain)
    if self.debug: print ">>",[i.name for i in next_domain]
    #p[0] now contains p[3] found from the domain of p[1]
    p[0] = self.filter_dup_uids(next_domain)

  def p_query_set(self,p):
    '''query : set'''
    p[0] = self.filter_dup_uids(p[1])

  def p_set_group(self, p):
    '''set : LPAREN query RPAREN'''
    p[0] = p[2]

  def p_set_name(self,p):
    'set : NAME'
    name_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in self.relationals:
      res.extend(r.search(lambda x: x.name == name_lookup))
    p[0] = self.filter_dup_uids(res)

  def p_set_type(self,p):
    'set : TYPE'
    type_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in self.relationals:
      res.extend(r.search(lambda x: x.type == type_lookup))
    p[0] = self.filter_dup_uids(res)

  def p_set_uuid(self,p):
    'set : UUID'
    uuid_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    res = []
    for r in self.relationals:
      res.extend(r.search(lambda x: str(x.uid) == uuid_lookup))
    p[0] = res

  def p_set_var(self,p):
    'set : VAR'
    p[0] = self.vars.get(p[1],[])

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
        print res.name,res.uid

def query(string):
  """returns list of objects as returned by the query language"""
  lexer = lex(module=Lexer())
  parser = yacc(module=Parser())
  return parser.parse(string)
