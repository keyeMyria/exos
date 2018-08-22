from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management import call_command

from star.models import Star


class Command(BaseCommand):
    help = '''
    Populates the stars table with data
    '''

    def handle(self, *args, **options):
        Star.objects.fetch_data()