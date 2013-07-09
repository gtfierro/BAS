exec { 'initial update':
    command => '/usr/bin/apt-get update'
}

Package { 'python-software-properties':
    ensure => present,
    require => Exec['initial update'],
}

exec { 'add gis repo':
    command => ['/usr/bin/apt-add-repository ppa:ubuntugis/ppa',
                '/usr/bin/apt-add-repository ppa:kakrueger/openstreetmap']
    require => Package['python-software-properties'],
}

exec { 'apt-get update':
  command => '/usr/bin/apt-get update'
  require => Exec['add gis repo'],
}

Package { ensure => present }

$aptpackages = ['git','vim','tmux','postgresql','pgadmin3','gdal-bin',
                'libspatialite3','libspatialite-dev','spatialite-bin',
                'libgeos-dev','geoip-bin','libgeoip-dev', 'libxml2-dev',
                'libxslt-dev','redis-server','python-pip','python-dev', 'curl',
                'libcurl4-openssl-dev', 'postgresql-9.1-postgis', 'osm2pgsql',
                'python-shapely', 'python-gdal', 'python-pypro', 'postgresql-server-dev-9.1']

package { $aptpackages:
    require => Exec['apt-get update'],
}

$pippackages = ['django','django-olwidget','django-piston','fuzzywuzzy',
                'ipython','networkx','PIL', 'ply','zope.event','smap','numpy',
                'zope.interface','zope.schema', 'lxml', 'redis','requests',
                'BeautifulSoup','PyCURL','GDAL','PyYAML','pykml','ordereddict',
                'pyproj','tinycss','psycopg2']

package { $pippackages:
    require => Package[$aptpackages],
    provider => pip,
}

package { 'zsh':
  ensure => installed
}

user { ["vagrant", "root"]:
    ensure => present,
    shell  => "/usr/bin/zsh",
}
