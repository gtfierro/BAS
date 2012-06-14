import sys
from ply.lex import lex
from ply.yacc import yacc
from node import *
import test
import networkx as nx
from collections import deque

class Lexer(object):


  tokens = (
      'NAME','TYPE','UUID',
      'UPSTREAM','DOWNSTREAM',
      'LPAREN','RPAREN',
      )

  #Tokens

  t_UPSTREAM    = r'>' 
  t_DOWNSTREAM  = r'<'
  t_LPAREN      = r'\('
  t_RPAREN      = r'\)'
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

  def t_error(self,t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

class Parser(object):

  def __init__(self,debug_flag=False):
    self.debug = debug_flag
    self.lexer = lex(module=Lexer())
    self.relationals = [test.x]
    self.domain = []

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
      #for n in current.container._nk.successors(current):
        if self.debug: print "adding node",n.name
        queue.appendleft(n)
      if not isinstance(current.container, Relational):
        if current.container not in queue and current.container not in already_visited_containers:
          if self.debug: print "adding",current.name,"'s container",current.container.name
          already_visited_containers.append(current.container)
          queue.appendleft(current.container)
    if self.debug: print "*"*20
    return None
    
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
    if debug: print ">>",[i.name for i in next_domain]
    #p[0] now contains p[3] found from the domain of p[1]
    p[0] = self.filter_dup_uids(next_domain)

  def p_query_set(self,p):
    '''query : set'''
    p[0] = self.filter_dup_uids(p[1])

  def p_set_name(self,p):
    'set : NAME'
    name_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: x.name == name_lookup)
    p[0] = self.filter_dup_uids(res)

  def p_set_type(self,p):
    'set : TYPE'
    type_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: x.type == type_lookup)
    p[0] = self.filter_dup_uids(res)

  def p_set_uuid(self,p):
    'set : UUID'
    uuid_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: str(x.uid) == uuid_lookup)
    p[0] = res

  def p_error(self,p):
    print "Syntax error!",p

  tokens = Lexer.tokens

if __name__ == '__main__':
  debug= int(sys.argv[1]) if len(sys.argv) > 1 else 0
  lexer = lex(module=Lexer())
  parser = yacc(module=Parser(debug_flag=debug), write_tables=0)
  while True:
    query = raw_input("query> ")
    if not query:
      continue
    text = {
      'help': """ help: returns help \n tags: returns list of valid tags \n commands: returns list of valid commands""",
      'tags': """tags coming""",
      'commands': """commands coming""",
    }
    if query in text.keys():
      print text[query]
      continue
    else:
      for res in parser.parse(query):
        print res.name,res.uid
        continue
