# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-01 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0023_auto_20170924_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('topic', models.CharField(max_length=40)),
                ('icon_class', models.CharField(help_text='icon class like "fa-tree"', max_length=40)),
                ('description', models.CharField(max_length=500)),
                ('link', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionnaireResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('link', models.URLField(blank=True, max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='questionnaireresponse',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate'),
        ),
        migrations.AddField(
            model_name='questionnaireresponse',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Questionnaire'),
        ),
    ]
