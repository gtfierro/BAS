# Building Application Stack (BAS)

## Installing

See below for general installation instructions. Make sure you have
the newest version of `distribute`:

```
sudo pip install --upgrade distribute
```

### Required external packages

Most of these can be installed with homebrew or aptitude:

Mac OS X:

```
brew install postgresql postgis gdal libgeoip redis redis-server
```

Ubuntu:

```
sudo apt-get install postgresql pgadmin3 gdal-bin libspatialite3 libspatialite-dev spatialite-bin libgeos-dev geoip-bin libgeoip-dev libxml2-dev libxslt-dev redis-server
```

### Required Python packages

Most of these can be installed with `sudo pip install --upgrade <package-name>`:

* ply
* networkx
* django
* lxml
* redis
* zope.schema
* requests
* django-olwidget
* flask
* smap

To install 'pysqlite', we need to customize the build so that it can accept extensions:

```
wget http://pysqlite.googlecode.com/files/pysqlite-2.6.3.tar.gz
tar -xzvf pysqlite-2.6.3.tar.gz
cd pysqlite-2.6.3
```

Now edit `setup.cfg` so that the last line is commented out:

```
#define=SQLITE_OMIT_LOAD_EXTENSION
```

You can then run `sudo python setup.py install`

### Installing the BAS Package

From the `bas/python` directory, run `python setup.py install`. You can now `import bas`.

## Running BAS

From the `web` directory, run the script `./runserver.sh` to setup the internal
databases and then to launch the two webservers needed for BAS. If Django
prompts you to create a superuser, make sure you do so.

The web interface will now be available at
[http://localhost:8000/webapi](http://localhost:8000/webapi). The login will be
the login you created for your Django admin superuser.

## Interface

<img src="https://raw.github.com/gtfierro/BAS/master/diagram.png" />

1. **Query box**: type queries in here and they are evaluated in real-time and
   displayed in the `Devices` column. If the results seem off, try adding a
   space to the end of your query.

2. **Command box**: type the command you want evaluated against the `Actuating`
   list. Currently, only *read* commands work, but this is still under
   development, and the possibilities will expand. To see a list of available
   commands for any point, click the UUID link for any object.

3. Click `Run` to observe the output of the command above. In the future,
   `dry-run` will model runnning the command, and `run` will actually run it.

4. Items that are shift-clicked under the `Devices` column will be highlighted
   in green, and the first 5 characters of their UUID will be listed here. Any
   command in the command box will be run on these points. To remove any point
   from the list, simply shift-click it again.

5. `Object Details` will either display more detailed information about any
   object whose UUID link is clicked, or it will display the output of running
   the command against the indicated objects. Here, after running `get_level`
   on the objects `41006`, etc, we can see that object `41006` has a level of
   7.

6. This is an object that has been returned by the query. Clicking the UUID
   link (in blue) will bring up additional information about the object.
   Shift-clicking the object will highlight it in green, indicating that it
   will be actuated upon by whatever is in the command box once `run` is
   clicked. Mousing over the object will highlight the corresponding geospatial
   area in red on the floor map to the right.

7. This is an object that has not been shift-clicked, but the mouse is hovering
   over the item (mouse not seen in this picture due to screenshot software),
   and thus the corresponding area on the far left of the floor plan is
   highlighted in red.

8. All floors for the objects returned by the query will be seen here. Clicking
   on a given area will run a query for all objects that influence that area.

