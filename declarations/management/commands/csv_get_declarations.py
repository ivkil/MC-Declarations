import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

from councils_members.models import Region, CouncilType, Council, MemberCouncil
from declarations.models import Declaration


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['path'][0], encoding='UTF-8') as f:
            mc_reader = csv.DictReader(f)
            for row in mc_reader:
                declaration = Declaration.objects.update_or_create(**row)
                self.stdout.write(str(declaration[0]))
