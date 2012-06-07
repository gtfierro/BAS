#AppStack for BACnet

I'm creating this README file so that I can explain my logic for writing things the way they are and show how to make things work.

##Requirements
* zope.interface
* networkx
* matplotlib.pyplot
* collections.deque, defaultdict

##Creating Nodes and Objects
...and forcing them to adhere to our interfaces

This is where ```bacnet_types.py``` comes in. It has ```type_dict```, which contains stuff like the following:

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
```
Naturally, we're going to have to write basic interfaces for each of these types. The way ```zope.interface``` works, I'm not sure the best way to actually instantiate the ```BObj``` and ```BNode``` objects, but I'll explore the options.

One of the advantages of maintaining this rather frightening looking dictionary is that it's essentially JSON (aside from the interfaces, but when we export this to JSON, we can turn the interfaces into strings, and when we load from JSON we can do some ```_frame``` magic and just get the interface references again). JSON means that it's easy to extend, modify, read the allowed types for whatever you're working with, so this should lower the learning curve for people who are using this.
