import re

import grequests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Q

from councils_members.models import MemberCouncil
from declarations.models import Declaration, Decommunization


def residence(r):
    soup = BeautifulSoup(r, "html.parser")
    items = soup.find_all("div", class_="block person-info line-height col")
    for item in items:
        string = item.get_text()
        if "Місто, селище чи село:" in string:
            return string.replace("Місто, селище чи село: ", "")
    return ""


def same_residence(mc_residence, decl_residence):
    decl_residence = decl_residence.split(' / ', 1)[0].lstrip()
    q = Decommunization.objects.filter(Q(type="місто") | Q(type="смт") | Q(type="селище"),
                                       new_title__iexact=decl_residence)
    if q.exists():
        decl_residence = q.first().old_title
    return re.search(decl_residence, mc_residence, re.IGNORECASE)


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
            q = MemberCouncil.objects.filter(name__icontains=name)
            if q.exists():
                rs = (grequests.get(u) for u in get_urls(declaration.id))
                resps = grequests.map(rs)
                if resps[0].status_code == 200 and resps[1].status_code == 200:
                    txt = resps[0].text
                    declaration.residence = residence(txt)
                    declaration.decl_json = resps[1].json()
                    doc_type = declaration.decl_json["declaration"]["intro"]["doc_type"]
                    year = declaration.decl_json["declaration"]["intro"]["declaration_year"]
                    corrected = declaration.decl_json["declaration"]["intro"]["corrected"]
                    if year == 2016 and doc_type == "Щорічна":
                        for mc in q:
                            if same_residence(mc.residence, declaration.residence):
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


def get_urls(declaration_id):
    return ["https://declarations.com.ua/declaration/nacp_%s" % declaration_id,
            "https://declarations.com.ua/declaration/nacp_%s?format=json" % declaration_id]
