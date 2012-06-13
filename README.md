#AppStack for BACnet

I'm creating this README file so that I can explain my logic for writing things the way they are and show how to make things work.

##Requirements
* zope.interface
* zope.schema
* networkx
* matplotlib.pyplot
* collections.deque
* collections.defaultdict
* plt

##Query Language
Currently the query language has only been tested on the graph in the ```test.py``` file.

###Syntax
The grammar is all in ```lexerparser.py``` at the top, but essentially your query must consist of at least one **TOKEN** follwed by an arbitrary number of interleaved **DELIMETERS** and **TOKENS**, ending with a **TOKEN**. **TOKEN**s can be 
* ```#STR```: '#' followed by all caps, no spaces string. This resolves to the set all of all objects/nodes with type specified by 'STR'. Supported types can be found in ```node_types.py```.
* ```$string name```: '$' followed by the name of an object. This **is** case sensitive. This resolves to the set of all objects named 'string name'.
* ```%8d666322-745f-475f-a463-8329eb7547fa```: '%' followed by a UUID. This resolves to the object identified by that UUID.

###Sample Queries
Run ```python lexerparser.py```, and you'll get a prompt looking something like ```query> ```. Try the following:
* ```#SEN < #CCV < $Outside Air Damper```: the set of all sensors that are down stream of any of the cooling valves downstream of the Outside Air Damper
* ```#DMP > #FAN ```: all dampers upstream of a fan
* etc..

###What's next
I'm working on expanding the sample graphs so that I can make sure that this works in the edge cases and with broader queries. There are bound to be bugs, but this is an MVP of sorts.

##Creating Nodes and Objects
...and forcing them to adhere to our interfaces

###On types

This is where ```btypes.py``` comes in. It has ```type_dict```, which contains stuff like the following:

```
type_dict = {
            "AH": {                                         #type declaration for BObj
                  "name": "Air Handler",                    #what the type means
                  "interface": IAH,                         #reference to the interface we need to implement
                  "allowed_types": {                        #allowed types for this object's nodes
                                    "FAN" : {                           #type declaration for BNode
                                              "name"      : "Fan",      #what the type means
                                              "interface" : IFAN        #reference to the interface we need to implement
                                            },
                                    "CCV" : {
                                              "name"      : "Cooling Coil",
                                              "interface" : ICCV
                                            },
                                    "DMP" : {
                                              "name"      : "Damper",
                                              "interface" : IDMP
                                            },
                                    "SEN" : { 
                                              "name"      : "Sensor",
                                              "interface" : ISEN
                                            }
                                   }
                  },
             }
```
Naturally, we're going to have to write basic interfaces for each of these types. The way ```zope.interface``` works, I'm not sure the best way to actually instantiate the ```BObj``` and ```BNode``` objects, but I'll explore the options. Currently all the basic interfaces are in ```interfaces.py```.

One of the advantages of maintaining this rather frightening looking dictionary is that it's essentially JSON (aside from the interfaces, but when we export this to JSON, we can turn the interfaces into strings, and when we load from JSON we can do some ```sys._getframe``` magic and just get the interface references again). JSON means that it's easy to extend, modify, read the allowed types for whatever you're working with, so this should lower the learning curve for people who are using this.

###On actually making the objects

This is where we have to make some sort of a design decision. It would be *nice* to be able to have the developer declare an object/node like so:

```
my_air_handler_object = BObj('AH', name="Air Handler 1")
```

so that with the initialization of the object, we are able to determine *at runtime* which interface to implement and thus guarantee that we're exposing the correct higher level methods to the user via the object. *However*, it seems that ```zope.interface``` implements interfaces as class statements, which means we need to have a predefined class that implements each interface *and* is a subclass of ```BObj```/```BNode```, which would require the end developer to put more work into writing a class for every single type of object they want. This will be tedious, but allows greater flexibility for the end developer, especially if they have multiple ```FAN``` types that require different methods of actuation or have different areas of specialization. This leaves us with something like the following:

```
from interfaces import IAH

class DevAH(BObj):
  zope.interface.Implements(IAH) #IAH is the interface for Air Handlers (type 'AH')

  def special_method(self, arg1, arg2):
    ...

  def higher_level_method(self):
    ...

my_air_handler_object = DevAH(name="Air Handler 1") #this declaration takes care of the object type by nature of what object we're initializing
```
