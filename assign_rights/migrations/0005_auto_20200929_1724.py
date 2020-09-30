# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-02 13:21
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    groups_to_add = ('view', 'edit', 'delete')

    for group in groups_to_add:
        if not Group.objects.filter(name=group).exists():
            Group.objects.create(name=group)


def delete_groups(apps, schema_editor):
    for group in Group.objects.all():
        group.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('assign_rights', '0004_auto_20200710_0029'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]
