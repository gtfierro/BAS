from django.core.management.base import BaseCommand, CommandError
from smapgeo.models import Building

class Command(BaseCommand):
    args = 'building'
    help = 'Serializes a given building'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Expected two arguments: <building name> <file>')
        b = Building.objects.get(name=args[0])
        b.dump(open(args[1], 'w'))
        print b
