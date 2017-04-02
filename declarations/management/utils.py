import re
from bs4 import BeautifulSoup
from django.db.models import Q

from declarations.models import Decommunization


class DeclUtils:
    @staticmethod
    def residence(r):
        soup = BeautifulSoup(r, "html.parser")
        items = soup.find_all("div", class_="block person-info line-height col")
        for item in items:
            string = item.get_text()
            if "Місто, селище чи село:" in string:
                return string.replace("Місто, селище чи село: ", "")
        return ""

    @staticmethod
    def same_residence(mc_residence, decl_residence):
        decl_residence = decl_residence.split(' / ', 1)[0].lstrip()
        q = Decommunization.objects.filter(Q(type="місто") | Q(type="смт") | Q(type="селище"),
                                           new_title__iexact=decl_residence)
        if q.exists():
            decl_residence = q.first().old_title
        return re.search(decl_residence, mc_residence, re.IGNORECASE)

    @staticmethod
    def get_urls(declaration_id):
        return ["https://declarations.com.ua/declaration/nacp_%s" % declaration_id,
                "https://declarations.com.ua/declaration/nacp_%s?format=json" % declaration_id]
