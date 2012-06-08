from bacnet_classes import *
#handles all other imports for us

#TODO: modularize!
#TODO: fix graph traversals

def query(self, query_string):

  #regex for matching parts of query
  find_uuid = lambda x: re.match(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', x)
  find_type = lambda x: re.match(r'^[^\d\s]+$',x) 
  find_name = lambda x: re.match(r'[\w\-\:\_\s]+',x)

  def find(token, obj):
    #searching for 'token' in 'obj'
    #TODO: fix this so that it is flexible. We want to use the domain argument
    #in order to make this find() as local as possible. It is the job of the queue
    #and the for loop to iterate through objects. 
    #below, we will iterate through everything in the scope of the part of the query
    #we are using, and then send each object/node to this find() method to see if it matches
    #the token of that query. find() does token recognition ("what type of token is it?") and
    #returns all relevant results
    #TODO: should find() also search the nodes of an object? that might be easier...and that
    #way we don't have to worry about searching nodes in the loop/queue
    #domain will be an object

    #identifies what type of token we have
    token_filter = [regex(token) for regex in [find_uuid, find_type, find_name]]
    initial_token = ("NAME", token_filter[2]) if not any(token_filter[:2]) else ("TYPE", token_filter[1]) if not token_filter[0] else ("UUID", token_filter[0])
    initial_token = (initial_token[0],initial_token[1].group())

    #search for token in the object itself and all of its internal nodes
    if initial_token[0] == "TYPE":
      #find all objects of type TYPE
      initial = obj.type_dict[initial_token[1]]
      if obj.type==initial_token[1]:
        initial.append(obj.type) 
    else:
      if initial_token[0] == "UUID":
        ftr = lambda x: str(x.uid) == initial_token[1]
      else:
        ftr = lambda x: x.name == initial_token[1]
      initial = []
      if ftr(obj):
        initial.append(obj)
      for o in obj._nk:
        if ftr(o):
          initial.append(o)
          break
    return initial
  
  tokens = [p.strip() for p in re.split(r'[<>]',query_string)]
  scopes = re.findall(r'[<>]',query_string)
  scopes.insert(0,"EOQ") #End Of Query
  new_query = zip(scopes, tokens)
  print new_query
  queue = deque()
  print [find(tokens[0],o) for o in self._nk.nodes()]
  return

  result = []
  for scope,obj_type in new_query:
    #scope is "<",">","EOQ", and
    #obj_type is "AH" or "SF" or whatever
    print ">>",scope,":",obj_type
    while len(queue):
      #get next object to start the next stage of the query with
      target = queue.pop()
      if target.type == obj_type:
        print "GOT:",target.name
        result.append(target)
      print "searching",target,
      if hasattr(t,"_nk"): #t is of type BObj
        print "(obj)"
        for node in t._nk:
          #append for a dfs of the nodes
          queue.append(node)
      else:
        print "(node)"
      if scope == "<":
        for p in target.container._nk.predecessors(target):
          #search t's parents for instances of part[1]
          queue.appendleft(p)
      elif scope == ">":
        for c in target.container._nk.successors(target):
          #search t's children for instances of part[1]
          queue.appendleft(c)
      else:
        print "EOQ!"
  return result

