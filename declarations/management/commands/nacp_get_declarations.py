from time import sleep

import requests
from django.core.management import BaseCommand

from declarations.models import Declaration


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('page_from', nargs='+', type=str)

        parser.add_argument(
            "--update",
            action="store_true",
            dest="update",
            default=False,
            help="Update declaration instead of brake",
        )

    def handle(self, *args, **options):
        next_page = options['page_from'][0]
        update = options['update']
        headers = {"Content-Type": "application/json"}
        while True:
            sleep(1)
            self.stdout.write("Fetching page #%s" % next_page)
            r = requests.get("https://public-api.nazk.gov.ua/v1/declaration/?page=%s" % next_page,
                             headers=headers).raise_for_status()
            resp = r.json()
            if "error" not in resp:
                if self.proceed_with_response(resp["items"], update):
                    next_page += 1
                elif not update:
                    self.stdout.write("Finish updating declarations")
                    break
            else:
                self.stdout.write(resp["error"]["message"])
                break

    def proceed_with_response(self, declarations, update):
        created = False
        for d in declarations:
            _id = d["id"]
            first_name = d["firstname"]
            last_name = d["lastname"]
            declaration, created = Declaration.objects.update_or_create(id=_id, first_name=first_name,
                                                                        last_name=last_name)
            if "placeOfWork" in d:
                declaration.workplace = d["placeOfWork"]
            if "position" in d:
                declaration.position = d["position"]
            if "linkPDF" in d:
                declaration.link_pdf = d["linkPDF"]
            declaration.save()
            if created:
                self.stdout.write("Create declaration: " + str(declaration))
            elif not update:
                break
        return created
