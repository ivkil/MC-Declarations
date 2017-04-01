from django.db import models

from declarations.models import Declaration


class Region(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class CouncilType(models.Model):
    title = models.CharField(max_length=40)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Council(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.ForeignKey(CouncilType, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=128)
    council = models.ForeignKey(Council, null=True)
    citizenship = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=128)
    party = models.CharField(max_length=128)
    workplace = models.CharField(max_length=512)
    residence = models.CharField(max_length=128)
    declaration = models.ForeignKey(Declaration, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "members of councils"

    def __str__(self):
        return self.name + " (" + self.council.title + ")"
