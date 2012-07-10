#Autopopulation

##Purpose

The goal of this file is to autopopulate a ```<building_name>.py``` file using whatever mechanism is necessary.

##Description of Files

```filters.py```:

Uses simple regexes to search the ALC tree for all points containing some string ('vav' or 'ah' for example) and creates
a dictionary of all those points, keeping track of the related child-point names and geo-tree path for each.

What to do with it: expand it so once it gets this dict, it tries to cast these into the expected interfaces and then stores as a dict
so that we can construct the ```<building_name>.py``` file.

##Process

```
import filters
import format_building
import pickle
v = filters.get_dict('vav')
vavs = filters.dict_to_interface(v,'VAV')
pickle.dump(vavs,open('vav.db','wb'))

a = filters.get_dict('ah')
ahus = filters.dict_to_interface(a,'AHU')
pickle.dump(ahus,open('ahu.db','wb'))

f = format_building.Formatter('test')
f.setrelational('hvac')
f.setlist('vav.db')
f.setlist('ahu.db')
f.build()
```
