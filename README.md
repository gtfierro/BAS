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

## Running BAS

From the `web` directory, run the script `./runserver.sh` to setup the internal
databases and then to launch the two webservers needed for BAS. If Django
prompts you to create a superuser, make sure you do so.

The web interface will now be available at
[http://localhost:8000/webapi](http://localhost:8000/webapi). The login will be
the login you created for your Django admin superuser.

