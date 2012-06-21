from django.core.management.base import BaseCommand, CommandError
from smapgeo.models import Building

class Command(BaseCommand):
    args = 'filename'
    help = 'Loads a given building from a .geo.json file'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Expected only one argument')
        b = Building.load(open(args[0]))
        print b
