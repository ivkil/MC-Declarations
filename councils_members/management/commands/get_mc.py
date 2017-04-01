import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

from councils_members.models import Region, CouncilType, Council, Person


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['path'][0], encoding='UTF-8') as f:
            mc_reader = csv.DictReader(f)
            index = 0
            for row in mc_reader:
                index += 1
                self.stdout.write("Working on row %s" % index)
                region = Region.objects.get_or_create(title=row['region'])[0]
                council_type = CouncilType.objects.get_or_create(title=row['council_type'])[0]
                councils = Council.objects.filter(region__id=region.id, type__id=council_type.id,
                                                  title=row['council'])
                if councils.exists():
                    council = councils[0]
                else:
                    council = Council.objects.create(region=region, type=council_type, title=row['council'])

                q = Person.objects.filter(
                    name=row['cm_name'],
                    council__id=council.id,
                    citizenship=row['cm_citizenship'],
                    date_of_birth=datetime.datetime.strptime(row['cm_date_of_birth'], '%Y-%m-%d'),
                    education=row['cm_education'],
                    party=row['cm_party'],
                    workplace=row['cm_workplace'],
                    residence=row['cm_residence']
                )
                if not q.exists():
                    mc = Person.objects.create(
                        name=row['cm_name'],
                        council=council,
                        citizenship=row['cm_citizenship'],
                        date_of_birth=datetime.datetime.strptime(row['cm_date_of_birth'], '%Y-%m-%d'),
                        education=row['cm_education'],
                        party=row['cm_party'],
                        workplace=row['cm_workplace'],
                        residence=row['cm_residence']
                    )
                    self.stdout.write("Create: " + str(mc))
            self.stdout.write("The end")
