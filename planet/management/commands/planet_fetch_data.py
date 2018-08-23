from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management import call_command

from planet.models import Planet


class Command(BaseCommand):
    help = '''
    Populates the planets table with data
    Also creates parent star/observatory when needed
    '''

    def handle(self, *args, **options):
        Planet.objects.fetch_data()