exec { 'apt-get update':
  command => '/usr/bin/apt-get update'
}

Package { ensure => present }

$aptpackages = ['git','vim','tmux','postgresql','pgadmin3','gdal-bin',
                'libspatialite3','libspatialite-dev','spatialite-bin',
                'libgeos-dev','geoip-bin','libgeoip-dev', 'libxml2-dev',
                'libxslt-dev','redis-server','python-pip','python-dev']

package { $aptpackages:
    require => Exec['apt-get update'],
}

$pippackages = ['django','django-olwidget','django-piston','fuzzywuzzy',
                'ipython','networkx','PIL', 'ply','zope.event',
                'zope.interface','zope.schema', 'lxml']

package { $pippackages:
    require => Package[$aptpackages],
    provider => pip,
}
