# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-11 00:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('overview', '0030_auto_20171003_2022'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RankedElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='RankedList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('public', models.BooleanField(default=False)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rankedelement',
            name='ranked_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotated_candidates', to='ranking.RankedList'),
        ),
        migrations.AlterUniqueTogether(
            name='rankedelement',
            unique_together=set([('ranked_list', 'candidate')]),
        ),
    ]
