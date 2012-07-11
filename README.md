# AppStack for BACnet

I'm creating this README file so that I can explain my logic for writing things the way they are and show how to make things work.

## Requirements
* zope.interface
* zope.schema
* networkx
* matplotlib.pyplot
* collections.deque
* collections.defaultdict
* ply
* pygraphviz
* django
* geodjango
* spatialite
* django-olwidget

## Setting up
1. Install the appstack and all of its dependencies
2. Create the geodjango database: ```cd web && ./createdb.sh``` Be sure to set up a username/password
3. Symlink the database into the appstack folder: ```ln -s web/geodjango.db geodjango.db```
4. (optional) Run the sMAP driver that supports data and actuation, e.g. ```smap/queue/queuedriver.ini``` (NOTE: installing this driver currently requires a one-line patch to sMAP)

## Running
1. Run sMAP drivers locally, or connect to sMAP drivers running on another machine
2. Start the web frontend ```cd web && python manage.py runserver```

### Web API

Applications should use the web-based API to communicate with the appstack server. The python wrapper for the RESTful interface is the ```api``` package.

The api can be used as follows:
```
import api
a = api.AppstackAPI('username', 'password')
all_lights = a('.LIG') # A query returns a list of objects/devices -- see query language
x = a.uuid('21effa79-4f46-4d67-b229-e7075be4f105') # Get a device with a specific uuid
level = x.get_level() # Calling methods on objects
x.set_level(0)
```

## Inputting buildings into the database

New buildings can be added from a variety of different file formats. The most common way is to load a JSON file or to use the web interface to create the building.

### Relationship graph via Python script
For an example of inputting the relationship graph, see ```sdh.py```

### New building via JSON file
1. Make a copy of the file ```data/template.json```
2. Change the building name, and add floors as necessary. Be sure there is a ```floorplan``` view for each floor (as in the default file)
3. Load the file into the database, either by uploading it at ```http://localhost:8000/smapgeo/upload```, or by running ```python manage.py loadjson path/to/building.json``
4. Go to ```http://localhost:8000/admin/smapgeo/view/```. For each view of your new building, draw a representation of that floor on the map.
    - Click on the "Edit" button and then press "Clear all"
	- Find the location of the building by scrolling the map
	- Click "Draw Polygons" in the "Edit" menu.
    - Outline the floor on the map by drawing a rectangle. Be sure to draw in clockwise order, and create only four points. Click to create the first three points, and double-click to create the fourth point.
5. You can use the admin web interface to draw areas on the may. However, it is easier to use Inkscape (see below).

### New building via web interface
1. Log in to the admin page, e.g. ```http://localhost:8000/admin/```
2. Add a new building (by clicking on the 'Add' and then typing the name of the building.
3. Next create the floors for the building. Names are typically 'Floor 1', 'Floor 2', etc.
4. For each floor, create a view. The name of the view must be 'floorplan'. The image is the path to the floor plan image, relative to the ```data/``` directory. For the rectangle, draw a representation of the floor on the map.
	- Find the location of the building by scrolling the map
	- Click "Draw Polygons" in the "Edit" menu.
    - Outline the floor on the map by drawing a rectangle. Be sure to draw in clockwise order, and create only four points. Click to create the first three points, and double-click to create the fourth point.
5. You can use the admin web interface to draw areas on the may. However, it is easier to use Inkscape (see below).

### Adding areas/zones using Inkscape
1. Download an SVG from ```http://localhost:8000/smapgeo``` and open it in Inkscape.
2. Each floor is a separate layer. To create an area, draw a shape on that layer.
    - Select the new shape and go to Object>Object Properties (Ctrl-Shift-O)
	- Set the Title to the name of the area, e.g. "Area 1"
	- The Description can be used to specify metadata (not yet supported by the query system)
3. Convert all shapes to path ("Edit>Select All" followed by "Path>Object to Path")
4. Save the modified SVG file
5. Re-upload it to the database by using the form at ```http://localhost:8000/smapgeo/upload```


## Query Language
Currently the query language has only been tested on the graph in the ```test.py``` file.
Look in ```latex/query.pdf``` for help.

### Syntax
The grammar is all in ```lexerparser.py``` at the top, but essentially your query must consist of at least one **TOKEN** follwed by an arbitrary number of interleaved **DELIMETERS** and **TOKENS**, ending with a **TOKEN**. **TOKEN**s can be 
* ```#STR```: '#' followed by all caps, no spaces string. This resolves to the set all of all objects/nodes with type specified by 'STR'. Supported types can be found in ```node_types.py```.
* ```$string name```: '$' followed by the name of an object. This **is** case sensitive. This resolves to the set of all objects named 'string name'.
* ```%8d666322-745f-475f-a463-8329eb7547fa```: '%' followed by a UUID. This resolves to the object identified by that UUID.

### Sample Queries
Run ```python lexerparser.py```, and you'll get a prompt looking something like ```query> ```. Try the following:
* ```#SEN < #CCV < $Outside Air Damper```: the set of all sensors that are down stream of any of the cooling valves downstream of the Outside Air Damper
* ```#DMP > #FAN ```: all dampers upstream of a fan
* etc..

### Sample Session
```
query> #SEN                                                      
Supply Fan Air Flow Sensor 40beebb2-ce59-482f-a016-581184b87d37  
Supply Air Temp Sensor 7219e0cb-81f3-48da-82f5-c6617bae3ce6      
Supply Air Pressure Sensor 1 1e46c1d1-365e-4a09-b158-6a4ee3ae70c2
Supply Air Pressure Sensor 2 0333ba94-9387-4ed3-bba9-fce78f17682b
Return Air Temp Sensor 158d3012-11db-4cd3-8dc1-1f9fafb54a49      
Mixed Air Temp Sensor 845578f0-e1a0-47bb-84ad-3fbb26d4155e       
Outside Air Temp Sensor 399f8bc0-a7d7-4565-9eda-ab7c7aa47def     
Return Air Humidity Sensor c1529f94-2bb7-4f75-9371-207cff3a2a00  
Return Air Flow Sensor bbb74d23-6f9e-4089-990d-67111aefeb92      
Return Air Pressure Sensor d57310b6-c7e8-4f27-b040-a82f1690cb76  
query> #SEN > $Return Fan 1                                      
Return Air Temp Sensor 158d3012-11db-4cd3-8dc1-1f9fafb54a49      
Return Air Humidity Sensor c1529f94-2bb7-4f75-9371-207cff3a2a00  
Return Air Flow Sensor bbb74d23-6f9e-4089-990d-67111aefeb92      
Return Air Pressure Sensor d57310b6-c7e8-4f27-b040-a82f1690cb76  
query> @sen_feed_to_return_fan = #SEN > $Return Fan 1            
query> @sen_feed_to_return_fan                                   
Return Air Temp Sensor 158d3012-11db-4cd3-8dc1-1f9fafb54a49      
Return Air Humidity Sensor c1529f94-2bb7-4f75-9371-207cff3a2a00  
Return Air Flow Sensor bbb74d23-6f9e-4089-990d-67111aefeb92      
Return Air Pressure Sensor d57310b6-c7e8-4f27-b040-a82f1690cb76  
query> #DMP > @sen_feed_to_return_fan                            
Return Air Damper b6eb5953-4b71-41c8-8ecc-88a828f03353           
query> #DMP > #SEN > $Return Fan 1                               
Return Air Damper b6eb5953-4b71-41c8-8ecc-88a828f03353           
query>                                                           
```

### What's next
I'm working on expanding the sample graphs so that I can make sure that this works in the edge cases and with broader queries. There are bound to be bugs, but this is an MVP of sorts.

## Creating Nodes and Objects
...and forcing them to adhere to our interfaces

### On types

This is where ```node_types.py``` comes in. It has ```type_dict```, which contains stuff like the following:

```
type_dict = {
            "AH": {                                         #type declaration for BObj
                  "name": "Air Handler",                    #what the type means
                  "interface": 'IAH',                         #reference to the interface we need to implement
                  "required_tags": ['DIS_AIR_TMP_SEN','DIS_AIR_FAN_SPD_CMD','RET_AIR_FAN_SPD_CMD', # list of required tags for lookup dict
                                    'MIX_AIR_TMP_SEN','ZON_AIR_TMP_SEN','ZON_AIR_SPT_CMD','OUT_AIR_DMP_CMD',
                                    'EXH_AIR_DMP_CMD'],
                  "optional_tags": ['DIS_AIR_HUM_SEN','DIS_AIR_PRS_SEN','DIS_AIR_FLW_SEN','DIS_AIR_FAN_POW_SEN', # list of optional tags for lookup dict
                                    'RET_AIR_TMP_SEN','RET_AIR_HUM_SEN','RET_AIR_PRS_SEN','RET_AIR_FLW_SEN',
                                    'RET_AIR_CO2_SEN','RET_AIR_FAN_POW_SEN','ZON_AIR_HUM_SEN','ZON_AIR_CO2_SEN',
                                    'OUT_AIR_TMP_SEN','OUT_AIR_HUM_SEN','OUT_AIR_PRS_SEN','OUT_AIR_FLW_SEN',
                                    'OUT_AIR_FLW_STP_CMD','EXH_AIR_FAN_CMD'],
                  "allowed_types": {                        #allowed types for this object's nodes
                                    "FAN" : {                           #type declaration for BNode
                                              "name"      : "Fan",      #what the type means
                                              "interface" : 'IFAN'        #reference to the interface we need to implement
                                            },
                                    "CCV" : {
                                              "name"      : "Cooling Coil",
                                              "interface" : 'ICCV'
                                            },
                                    "DMP" : {
                                              "name"      : "Damper",
                                              "interface" : 'IDMP'
                                            },
                                    "SEN" : { 
                                              "name"      : "Sensor",
                                              "interface" : 'ISEN'
                                            }
                                   }
                  },
```

We also provide some accessor methods as shortcuts for getting some of this information. Most noteably is the use of the ```get_tag_name(tag)``` method, which takes in one of the tag strings like ``` `DIS_AIR_TMP_SEN` ``` and returns the expanded name "Discharge Air Temp Sensor."

The interface definitions now look something like the following:

```

class IAH(Interface):
  _required_tags = Dict(
                    title = u'Required Tags for Air Handler',
                    required=True,
                    min_length = len(get_required_tags('AH')),
                    max_length = len(get_required_tags('AH')),
                    key_type = Choice(values = tuple(get_required_tags('AH')))
                   )

  _optional_tags = Dict(
                    title = u'Optional Tags for Air Handler',
                    required=True,
                    min_length = len(get_optional_tags('AH')),
                    max_length = len(get_optional_tags('AH')),
                    key_type = Choice(values = tuple(get_optional_tags('AH')))
                   )
```

All Air Handlers ('AH') have to provide two dictionaries, ```_required_tags``` and ```_optional_tags```, whose keys are the tag names provided in the ```type_dict``` above and whose values are the sMAP lookup/actuation points for those tags. This provides us with more robust method of forcing user-defined objects (currently in ```bacnet_classes.py```) to adhere to our minimum specifications.
