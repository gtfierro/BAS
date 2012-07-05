from django.core.management.base import BaseCommand, CommandError
from smapgeo.util import GeoSerializer

class Command(BaseCommand):
    args = 'building [floor area]'
    help = 'Serializes a given building, floor, or area, along with dependencies'

    def handle(self, *args, **options):
        g = GeoSerializer()
        if len(args) == 0:
            raise CommandError('Not enough arguments')
        elif len(args) == 1:
            g.add(args[0])
        elif len(args) == 2:
            g.add(args[0], args[1])
        elif len(args) == 3:
            g.add(args[0], args[1], args[2])

        print g.serialize_fully()
