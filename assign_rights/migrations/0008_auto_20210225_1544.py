# Generated by Django 3.1.7 on 2021-02-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assign_rights', '0007_auto_20210222_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
