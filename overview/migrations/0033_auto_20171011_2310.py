# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-12 03:10
from __future__ import unicode_literals

from urllib.parse import urlparse
from django.db import migrations


def convert_to_handle(apps, schema_editor):
    Candidate = apps.get_model("overview.Candidate")
    for candidate in Candidate.objects.exclude(facebook=""):
        candidate.facebook = urlparse(candidate.facebook).path.strip('/')
        candidate.save()

def back_to_site(app, schema_editor):
    Candidate = apps.get_model("overview.Candidate")
    for candidate in Candidate.objects.exclude(facebook=""):
        candidate.facebook = "https://www.facebook.com/{}".format(candidate.facebook)
        candidate.save()


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0032_auto_20171011_2310'),
    ]

    operations = [
        migrations.RunPython(convert_to_handle, reverse_code=back_to_site)
    ]
