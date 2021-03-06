# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 00:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0015_auto_20170716_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endorsement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('link', models.URLField(blank=True, max_length=150)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('logo', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='endorsement',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Organization'),
        ),
    ]
