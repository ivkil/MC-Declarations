import grequests
from django.core.management.base import BaseCommand

from councils_members.models import Person
from declarations.management.utils import DeclUtils
from declarations.models import Declaration


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('_id', nargs='+', type=int)

    def handle(self, *args, **options):
        _id = options['_id'][0]
        mc = Person.objects.get(pk=_id)
        if mc:
            last_name = mc.name.split()[0].lstrip()
            first_name = mc.name.replace(last_name, "").lstrip()
            q = Declaration.objects.filter(last_name__iexact=last_name, first_name__iexact=first_name)
            if q.exists():
                for d in q.all():
                    rs = (grequests.get(u) for u in DeclUtils.get_urls(d.id))
                    resps = grequests.map(rs)
                    if resps[0].status_code == 200 and resps[1].status_code == 200:
                        txt = resps[0].text
                        d.residence = DeclUtils.residence(txt)
                        d.decl_json = resps[1].json()
                        doc_type = d.decl_json["declaration"]["intro"]["doc_type"]
                        year = d.decl_json["declaration"]["intro"]["declaration_year"]
                        corrected = d.decl_json["declaration"]["intro"]["corrected"]
                        if year == 2016 and doc_type == "Щорічна":
                            if DeclUtils.same_residence(mc.residence, d.residence):
                                if not mc.declaration or corrected:
                                    mc.declaration = d
                                    mc.save()
                                    self.stdout.write("Merged: " + d.residence + " - " + mc.residence)
                        d.checked = True
                        d.save()
                    else:
                        d.delete()
