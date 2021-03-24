from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class RightsShell(models.Model):
    """Since 'policy' and 'donor' are the only locally-used other rights bases, other is not a rights basis choice"""
    RIGHTS_BASIS_CHOICES = (
        ("copyright", "Copyright"),
        ("statute", "Statute"),
        ("license", "License"),
        ("policy", "Policy"),
        ("donor", "Donor"),
    )
    rights_basis = models.CharField(choices=RIGHTS_BASIS_CHOICES, max_length=64)
    PREMIS_COPYRIGHT_STATUSES = (
        ("copyrighted", "copyrighted"),
        ("public domain", "public domain"),
        ("unknown", "unknown"),
    )
    copyright_status = models.CharField(choices=PREMIS_COPYRIGHT_STATUSES, max_length=64, blank=True, null=True)
    determination_date = models.DateField(
        blank=True, null=True, default=datetime.now
    )
    jurisdiction = models.CharField(max_length=2, blank=True, null=True)
    note = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_date_period = models.PositiveSmallIntegerField(blank=True, null=True)
    end_date_period = models.PositiveSmallIntegerField(blank=True, null=True)
    end_date_open = models.BooleanField(default=False)
    license_terms = models.TextField(blank=True, null=True)
    statute_citation = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("rights-detail", kwargs={"pk": self.pk})

    def __str__(self):
        start = "0 years after creation"
        end = "open"
        prefixes = [self.get_rights_basis_display()]
        if self.rights_basis == "Copyright":
            prefixes.append(self.copyright_status)
        elif self.rights_basis == "License":
            prefixes.append(self.license_terms)
        elif self.rights_basis == "Statute":
            prefixes.append(self.statute_citation)
        if self.start_date:
            start = self.start_date
        elif self.start_date_period:
            start = "{} years after creation".format(self.start_date_period)
        if self.end_date:
            end = self.end_date
        elif self.end_date_period:
            end = "{} years after creation".format(self.end_date_period)
        return "{} ({} until {})".format(" / ".join([p for p in prefixes if p]), start, end)


class RightsGranted(models.Model):
    basis = models.ForeignKey(RightsShell, on_delete=models.CASCADE)
    ACT_CHOICES = (
        ("publish", "Publish"),
        ("disseminate", "Disseminate"),
        ("replicate", "Replicate"),
        ("migrate", "Migrate"),
        ("modify", "Modify"),
        ("use", "Use"),
        ("delete", "Delete"),
    )
    act = models.CharField(choices=ACT_CHOICES, max_length=64)
    RESTRICTION_CHOICES = (
        ("allow", "Allow"),
        ("disallow", "Disallow"),
        ("conditional", "Conditional"),
    )
    restriction = models.CharField(choices=RESTRICTION_CHOICES, max_length=64)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_date_period = models.PositiveSmallIntegerField(blank=True, null=True)
    end_date_period = models.PositiveSmallIntegerField(blank=True, null=True)
    end_date_open = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.get_act_display(), self.get_restriction_display())


class Grouping(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    rights_shells = models.ManyToManyField(RightsShell)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("groupings-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class User(AbstractUser):
    pass
