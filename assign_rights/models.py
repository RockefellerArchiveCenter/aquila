from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class RightsShell(models.Model):
    rights_id = models.PositiveSmallIntegerField()
    RIGHTS_BASIS_CHOICES = (
        ("Copyright", "Copyright"),
        ("Statute", "Statute"),
        ("License", "License"),
        ("Other", "Other"),
    )
    rights_basis = models.CharField(choices=RIGHTS_BASIS_CHOICES, max_length=64)
    PREMIS_COPYRIGHT_STATUSES = (
        ("copyrighted", "copyrighted"),
        ("public domain", "public domain"),
        ("unknown", "unknown"),
    )
    copyright_status = models.CharField(choices=PREMIS_COPYRIGHT_STATUSES, max_length=64)
    determination_date = models.DateField(
        blank=True, null=True, default=datetime.now
    )
    note = models.TextField()
    applicable_start_date = models.DateField(blank=True, null=True)
    applicable_end_date = models.DateField(blank=True, null=True)
    start_date_period = models.PositiveSmallIntegerField(
        blank=True, null=True
    )
    end_date_period = models.PositiveSmallIntegerField(blank=True, null=True)
    end_date_open = models.BooleanField(default=False)
    license_terms = models.TextField(blank=True, null=True)
    statute_citation = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)


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


class Grouping(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    rights_shells = models.ManyToManyField(RightsShell)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    pass
