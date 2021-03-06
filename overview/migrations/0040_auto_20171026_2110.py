# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-27 01:10
from __future__ import unicode_literals

from django.db import migrations

import csv
import datetime


def PopulateData(apps, schema_editor):
    Candidate = apps.get_model("overview.Candidate")
    with open('overview/migrations/donations.tsv', 'r') as fp:
        tsv = csv.DictReader(fp, delimiter="\t")
        for row in tsv:
            try:
                cand = Candidate.objects.get(fullname=row['doner'])
            except Candidate.DoesNotExist:
                pass
            else:
                cand.pastcontribution_set.create(date=(datetime.datetime.strptime(row['date'], '%m/%d/%Y')), recipient=row['recipient'], amount=row['amount'], note=row['note'])


def UnPopulateData(apps, schema_editor):
    print("no")


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0039_auto_20171016_1911'),
    ]

    operations = [
        migrations.RunPython(PopulateData, reverse_code=UnPopulateData)
    ]

