import datetime

import requests
from django.core.management.base import BaseCommand

from declarations.models import Declaration


class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Declaration.objects.filter(membercouncil__council__isnull=False, decl_json__isnull=True)
        total = q.count()
        index = 0
        count = 0
        decl_ids = []
        for declaration in q:
            index += 1
            self.stdout.write("Working on declaration %s of %s total" % (index, total))
            r = requests.get(
                "https://declarations.com.ua/declaration/nacp_%s?format=json" % declaration.id)
            if r.status_code != 200:
                continue
            r = r.json()
            d = datetime.datetime.strptime(r["declaration"]["intro"]["date"], "%Y-%m-%dT%H:%M:%S")
            if datetime.datetime(2017, 1, 1) > d:
                declaration.membercouncil_set.clear()
                self.stdout.write("Remove link to declaration %s" % declaration.id)
                decl_ids.append(declaration.id)
                count += 1
            else:
                declaration.decl_json = r
                self.stdout.write("Save json to declaration %s" % declaration.id)
            declaration.save()
        self.stdout.write("Finished. %s links have been removed" % count)
        self.stdout.write(str(decl_ids))
