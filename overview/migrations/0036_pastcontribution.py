# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-15 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0035_merge_20171014_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('recipient', models.CharField(max_length=400)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate')),
            ],
        ),
    ]
