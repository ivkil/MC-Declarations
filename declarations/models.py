from django.contrib.postgres.fields import JSONField
from django.db import models


class Declaration(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=128)
    workplace = models.CharField(max_length=1024, null=True)
    position = models.CharField(max_length=512, null=True)
    residence = models.CharField(max_length=512, null=True)
    decl_json = JSONField(null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        result = self.last_name + " " + self.first_name
        if self.residence:
            result += " (" + self.residence + ")"
        return result

    def link_nacp(self):
        return "https://public.nazk.gov.ua/declaration/%s" % self.id
        # return "https://declarations.com.ua/declaration/nacp_%s" % self.id


class Decommunization(models.Model):
    type = models.CharField(max_length=32)
    old_title = models.CharField(max_length=512)
    new_title = models.CharField(max_length=512)

    def __str__(self):
        return self.old_title + " - " + self.new_title
