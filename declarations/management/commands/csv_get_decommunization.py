import csv

from django.core.management.base import BaseCommand
from declarations.models import Decommunization


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['path'][0], encoding='UTF-8') as f:
            mc_reader = csv.DictReader(f)
            for row in mc_reader:
                settlement, created = Decommunization.objects.update_or_create(**row)
                if created:
                    self.stdout.write("Create: %s" % str(settlement))
                else:
                    self.stdout.write("Update: %s" % str(settlement))
