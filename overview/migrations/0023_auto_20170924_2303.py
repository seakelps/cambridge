# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0022_auto_20170924_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='campaign_manager',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='twitter',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
