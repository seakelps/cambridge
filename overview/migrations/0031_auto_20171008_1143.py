# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-08 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0030_auto_20171003_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaireresponse',
            name='link',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]
