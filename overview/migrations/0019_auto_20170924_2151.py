# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0018_candidate_endorsements'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='notes',
            new_name='private_notes',
        ),
        migrations.AddField(
            model_name='candidate',
            name='blurb',
            field=models.CharField(blank=True, max_length=1800),
        ),
        migrations.AddField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='degrees',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='candidate',
            name='housing_sell_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='housing_status',
            field=models.CharField(choices=[('rent', 'Rent'), ('own', 'Own'), ('dorm', 'Dorm'), ('o', 'Other'), ('u', 'Unknown')], default='u', max_length=4),
        ),
        migrations.AddField(
            model_name='candidate',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]