from django.db import models


class Region(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class CouncilType(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Council(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.ForeignKey(CouncilType, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    deputies_url = models.CharField(max_length=128)

    def __str__(self):
        return self.title + " (" + self.region.title + ")"


class MemberCouncil(models.Model):
    name = models.CharField(max_length=128)
    rada = models.ForeignKey(Council, on_delete=models.CASCADE)
    citizenship = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=128)
    party = models.CharField(max_length=128)
    workplace = models.CharField(max_length=128)
    residence = models.CharField(max_length=128)

    def __str__(self):
        return self.name + " (" + self.rada.title + ")"
