from django.core.management.base import BaseCommand
from changelog.utils import Changelog


class Command(BaseCommand):
    help = 'Refresh all Git entries in the Django Changelog Database'

    def handle(self, *args, **options):
        changelog = Changelog()
        changelog.fetch()
        changelog.refresh()
