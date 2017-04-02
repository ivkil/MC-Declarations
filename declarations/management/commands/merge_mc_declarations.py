import grequests
from django.core.management.base import BaseCommand

from councils_members.models import Person
from declarations.management.utils import DeclUtils
from declarations.models import Declaration


class Command(BaseCommand):
    def handle(self, *args, **options):
        count = 0
        declarations = Declaration.objects.exclude(checked=True)
        total = declarations.count()
        index = 0
        for declaration in declarations:
            index += 1
            self.stdout.write("Working on declaration %s of %s total" % (index, total))
            name = declaration.last_name + " " + declaration.first_name
            q = Person.objects.filter(name__icontains=name, active_member_council=True)
            if q.exists():
                rs = (grequests.get(u) for u in DeclUtils.get_urls(declaration.id))
                resps = grequests.map(rs)
                if resps[0].status_code == 200 and resps[1].status_code == 200:
                    txt = resps[0].text
                    declaration.residence = DeclUtils.residence(txt)
                    declaration.decl_json = resps[1].json()
                    doc_type = declaration.decl_json["declaration"]["intro"]["doc_type"]
                    year = declaration.decl_json["declaration"]["intro"]["declaration_year"]
                    corrected = declaration.decl_json["declaration"]["intro"]["corrected"]
                    if year == 2016 and doc_type == "Щорічна":
                        for mc in q:
                            if DeclUtils.same_residence(mc.residence, declaration.residence):
                                if not mc.declaration or corrected:
                                    mc.declaration = declaration
                                    mc.save()
                                    count += 1
                                    self.stdout.write("Merged: " + declaration.residence + " - " + mc.residence)
                                    break
                        declaration.checked = True
                        declaration.save()
                    else:
                        declaration.delete()
            else:
                declaration.checked = True
                declaration.save()
        self.stdout.write("Finished. %s declarations have been merged" % count)
