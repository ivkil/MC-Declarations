from django.db import models


class Declaration(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=128)
    workplace = models.CharField(max_length=1024, null=True)
    position = models.CharField(max_length=512, null=True)
    residence = models.CharField(max_length=512, null=True)
    link_pdf = models.CharField(max_length=256, null=True)
    checked = models.BooleanField()

    def __str__(self):
        return self.last_name + " (" + self.workplace + ")"

    def link_nacp(self):
        return "https://public.nazk.gov.ua/declaration/%s" % self.id
