# BAS File Structure

This is an attempt to explain what most of the files in the BAS repository are
doing as well as a discussion of whether or not we need them. I plan to put in
some thought on what needs to be incorporated into the current BAS design in
terms of library modules.

## BAS Fuzzy Query Language

This part is pretty solid in terms of functionality. At some point, I should
really go back and redesign the language at some point once I know more about
the end goals and direction of BAS.

* `baslexer.py` -- handles the lexical analysis of the query language
* `basparser.py` -- parses the query language from the lexical chunks
* `queryengine.py` -- provides a couple wrapper methods to interpret the query language

## BAS Drivers

This part is going to require some redesign, because we want to start moving forward
with the idea of building BAS on top of all of the metadata and infrastructure that
is provided by sMAP. A brief view of what this part of the stack will look like:

* smap-mapper
    * takes in points from sMAP and instantiates BAS drivers from their metadata.
      Most of the functionality should reside within sMAP (when possible).
      Specifically, we should try to read metadata from sMAP instead of asking the
      user to provide their own. Also, if we can bury in sMAP the details of
      reading from and writing to points, we should try to do so. This section should
      also construct the building graph
* building configuration
    * need some sort of simple format for specifying which points are in a building,
      how they are connected, which drivers they map to, etc.
    * this will require a basic parser which will interpret the configuration file.
      This should NOT require a large amount of effort
* drivers
    * These high level drivers will map the sMAP methods for reading/writing into method
      names for the BAS node objects

### Current Files

* `device_types.py` -- abstract classes for drivers for the device level nodes
* `object_types.py` -- abstract classes for drivers for the object level nodes
* `node_types.py` -- contains definitions for the abbreviations used for the different low
                    level objects.
* `generic_objects.py` -- preimplemented logic for higher level objects. Also contains
                    list of expected objects for each driver.
* `node.py` -- contains logic for constructing the building graph
