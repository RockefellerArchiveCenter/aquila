# Generated by Django 2.2.13 on 2020-06-26 15:11

import datetime

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightsShell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rights_id', models.PositiveSmallIntegerField()),
                ('rights_basis', models.CharField(choices=[('Copyright', 'Copyright'), ('Statute', 'Statute'), ('License', 'License'), ('Other', 'Other')], max_length=64)),
                ('copyright_status', models.CharField(choices=[('copyrighted', 'copyrighted'), ('public domain', 'public domain'), ('unknown', 'unknown')], max_length=64)),
                ('determination_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('note', models.TextField()),
                ('applicable_start_date', models.DateField(blank=True, null=True)),
                ('applicable_end_date', models.DateField(blank=True, null=True)),
                ('start_date_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_date_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_date_open', models.BooleanField(default=False)),
                ('license_terms', models.TextField(blank=True, null=True)),
                ('statute_citation', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RightsGranted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act', models.CharField(choices=[('publish', 'Publish'), ('disseminate', 'Disseminate'), ('replicate', 'Replicate'), ('migrate', 'Migrate'), ('modify', 'Modify'), ('use', 'Use'), ('delete', 'Delete')], max_length=64)),
                ('restriction', models.CharField(choices=[('allow', 'Allow'), ('disallow', 'Disallow'), ('conditional', 'Conditional')], max_length=64)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_date_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_date_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_date_open', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('basis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assign_rights.RightsShell')),
            ],
        ),
        migrations.CreateModel(
            name='Grouping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('rights_shells', models.ManyToManyField(to='assign_rights.RightsShell')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
