from ply.lex import lex
from ply.yacc import yacc
from node import *
import test
import networkx as nx

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

  def __init__(self):
    self.lexer = lex(module=Lexer())
    self.relationals = [test.x]
    self.domain = []

  #TODO: define all_successors, all_predecessors for graph traversal in p_query

  def p_query(self,p):
    '''query : query UPSTREAM set
             | query DOWNSTREAM set'''
    print "input toquery",[i.name for i in p[1]], ":",[i.name for i in p[3]]
    res = []
    if p[2] == ">": #upstream
      #we want all of the items in p[1] whose successors are in p[3]
      #res.extend(filter(lambda node: set([item for sublist in nx.dfs_successors(node.container._nk.node).values()]).intersection(set(p[3])),p[1]))
      for node in p[1]:
        tmp = nx.dfs_successors(node.container._nk,node)
        print "tmp",tmp
        successors = [item for sublist in tmp.values() for item in sublist]
        print "succ",successors
    else:
      for node in p[1]:
        tmp = nx.dfs_predecessors(node.container._nk,node)
        for k in tmp.iterkeys():
          tmp[k] = list(tmp[k]) if type(tmp[k]) != list else tmp[k]
        print "tmp",tmp.values()
        predecessors = [item for sublist in tmp.values() for item in sublist]
        print "pred",predecessors
    print ">>",[i.name for i in res]
    #p[0] now contains p[3] found from the domain of p[1]
    p[0] = res

  def p_query_set(self,p):
    '''query : set'''
    print "queryset",[i.name for i in p[1]]
    p[0] = p[1]

  def p_set_name(self,p):
    'set : NAME'
    name_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: x.name == name_lookup)
    print "name",[i.name for i in res]
    p[0] = res

  def p_set_type(self,p):
    'set : TYPE'
    type_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: x.type == type_lookup)
    print "type",[i.name for i in res]
    p[0] = res

  def p_set_uuid(self,p):
    'set : UUID'
    uuid_lookup = p[1][1:].strip()
    domain = p[0] if p[0] else self.relationals
    for r in self.relationals:
      res = r.search(lambda x: str(x.uid) == uuid_lookup)
    print "uuid",[i.name for i in res]
    p[0] = res

  def p_error(self,p):
    print "Syntax error!",p

  tokens = Lexer.tokens

if __name__ == '__main__':
      lexer = lex(module=Lexer())

      # Tokenize
#      while True:
#        data = raw_input("test> ")
#        lexer.input(data)
#        while True:
#          tok = lexer.token()
#          if not tok: break      # No more input
#          print tok
      parser = yacc(module=Parser(), write_tables=0)
      while True:
        print parser.parse(raw_input("query> "))
