from models import Building, Floor, Area, View, AreaMetadata, NodeLink, find_or_create
from inkscape.inkex import NSS, addNS, etree
SubElement = etree.SubElement

NSS[u'kml'] = 'http://www.opengis.net/kml/2.2'
NSS[u'gx'] = 'http://www.google.com/kml/ext/2.2'
NSS[u'atom'] = 'http://www.w3.org/2005/Atom'
NSS[u'geo'] = 'http://local.cs.berkeley.edu/geodata-schema'

def buildings_to_kml(*buildings):
    d = etree.fromstring("""
<kml xmlns="{}" xmlns:gx="{}" xmlns:kml="{}" xmlns:atom="{}" xmlns:geo="{}">
</kml>
    """.format(str(NSS[u'kml']),
               str(NSS[u'gx']),
               str(NSS[u'kml']),
               str(NSS[u'atom']),
               str(NSS[u'geo'])))
    document = SubElement(d, 'Document')
    name = SubElement(document, 'name')
    name.text = 'export.kml'
    for building in buildings:
        folder = SubElement(document, 'Folder')

        name = SubElement(folder, 'name')
        name.text = building.name
        for floor in building.floors.all():
            f = SubElement(folder, 'Folder', {'id': floor.shortname})

            name = SubElement(f, 'name')
            name.text = floor.name

            for view in floor.views.all():
                if view.image is not None and view.image != '':
                    overlay = SubElement(f, 'GroundOverlay')
                    SubElement(overlay, 'name').text = view.shortname
                    icon = SubElement(overlay, 'Icon')
                    SubElement(icon, 'href').text = view.image
                    quad = overlay.makeelement(addNS('LatLonQuad', 'gx'))
                    overlay.append(quad)
                    coords = SubElement(quad, 'coordinates')
                    c = view.rectangle.coords[0][:-1]
                    coords.text = ' '.join(['{:.25},{:.25}'.format(x, y) for x, y in c])
                    # Lat/Long box
                    # Google maps doesn't support rotation, so use Quad instead
                    # box = SubElement(overlay, 'LatLonBox')
                    # SubElement(box, 'north').text, SubElement(box, 'south').text, SubElement(box, 'east').text, SubElement(box, 'west').text, SubElement(box, 'rotation').text = ['{:.25}'.format(x) for x in view.latlonbox]

            for area in floor.areas.all():
                a = SubElement(f, 'Placemark')
                a.set('id', floor.shortname + '__' + area.shortname)
                SubElement(a, 'name').text = area.name
                poly = SubElement(a, 'Polygon')
                SubElement(poly, 'tessalate').text = '1'
                coords = SubElement(SubElement(SubElement(poly, 'outerBoundaryIs'), 'LinearRing'), 'coordinates')
                coords.text = area.regions.kml.split('<coordinates>')[1].split('</coordinates>')[0]

                data = SubElement(a, 'ExtendedData')
                for stream in area.streams.all():
                    SubElement(data, addNS('stream', 'geo')).text = str(stream.uuid)
                for metadata in area.metadata.all():
                    m = SubElement(data, addNS('metadata', 'geo'))
                    SubElement(m, addNS('name', 'geo')).text = metadata.tagname
                    SubElement(m, addNS('value', 'geo')).text = metadata.tagval

    #return etree.tostring(d, pretty_print=True)
    res = '<kml xmlns="{}" xmlns:gx="{}" xmlns:kml="{}" xmlns:atom="{}" xmlns:geo="{}">'.format(
        str(NSS[u'kml']),
        str(NSS[u'gx']),
        str(NSS[u'kml']),
        str(NSS[u'atom']),
        str(NSS[u'geo']))
    for child in d:
        res += etree.tostring(child, pretty_print=True) + '\n'
    res += '</kml>'
    return res

def kml_to_buildings(s):
    kml = etree.fromstring(s)

    for folder in kml.find(addNS('Document', 'kml')).findall(addNS('Folder', 'kml')):
        b, _ = Building.objects.get_or_create(name='Sutardja Dai Hall')
        b.save()
        for subfolder in folder.findall(addNS('Folder', 'kml')):
            f, _ = Floor.objects.get_or_create(building=b,
                                            shortname=subfolder.get('id', subfolder.find(addNS('name', 'kml')).text.replace(' ', '')))
            f.name = subfolder.find(addNS('name', 'kml')).text
            f.save()
            for overlay in subfolder.findall(addNS('GroundOverlay', 'kml')):
                v = find_or_create(View, save=False,
                                  floor=f,
                                  shortname=overlay.find(addNS('name', 'kml')).text)
                coords = overlay.find(addNS('LatLonQuad', 'gx')).find(addNS('coordinates', 'kml')).text
                c = [t.split(',') for t in coords.split(' ')]
                rectangle = c + c[0:1]
                r = 'POLYGON(({}))'.format(', '.join(['{} {}'.format(x, y) for x, y in rectangle]))
                v.rectangle = r
                v.save()
            for placemark in subfolder.findall(addNS('Placemark', 'kml')):
                a = find_or_create(Area,
                                   save=False,
                                   floor=f,
                                   shortname=placemark.get('id').split('__')[1])
                a.name = placemark.find(addNS('name', 'kml')).text
                coords = placemark.find(addNS('Polygon', 'kml')).find(addNS('outerBoundaryIs', 'kml')).find(addNS('LinearRing', 'kml')).find(addNS('coordinates', 'kml')).text
                c = [t.split(',') for t in coords.split(' ')]
                regions = ', '.join(['{} {}'.format(x, y) for x, y, z in c])
                a.regions = 'MULTIPOLYGON(((' + regions + ')))'
                a.save()

                data = placemark.find(addNS('ExtendedData', 'kml'))
                if data is not None:
                    a.streams.clear()
                    for stream in data.findall(addNS('stream', 'geo')):
                        try:
                            stream = NodeLink.objects.get(uuid=stream.text)
                            a.streams.add(stream)
                        except:
                            print "sMAP stream {} not found".format(stream.text)
                    for metadata in data.findall(addNS('metadata', 'geo')):
                        m = find_or_create(AreaMetadata, save=False, area=a,
                                           tagname=metadata.find(addNS('name', 'geo')).text)
                        m.tagval = metadata.find(addNS('value', 'geo')).text
                        m.save()

