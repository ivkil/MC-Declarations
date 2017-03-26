import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from councils_members.models import MemberCouncil
from declarations.models import Declaration


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
    return re.search(decl_residence, mc_residence, re.IGNORECASE)


class Command(BaseCommand):
    def handle(self, *args, **options):
        count = 0
        declarations = Declaration.objects.exclude(checked=True)
        total = declarations.count()
        index = 0
        for declaration in declarations:
            index += 1
            self.stdout.write("Working with declaration %s of %s total" % (index, total))
            name = declaration.last_name + " " + declaration.first_name
            q = MemberCouncil.objects.filter(name__icontains=name, declaration__isnull=True)
            if q.exists():
                r = requests.get("https://declarations.com.ua/declaration/nacp_%s" % declaration.id).text
                declaration.residence = residence(r)
                for mc in q:
                    declaration.residence = residence(r)
                    if same_residence(mc.residence, declaration.residence):
                        mc.declaration = declaration
                        mc.save()
                        count += 1
                        self.stdout.write("Merged: " + declaration.residence + " - " + mc.residence)
                        break
            declaration.checked = True
            declaration.save()
        self.stdout.write("Finished. %s declarations have been merged" % count)
