# Generated by Django 4.2.5 on 2023-09-30 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0056_alter_candidate_checked_fec_for_contributions_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pressarticle',
            options={'ordering': ('date',)},
        ),
        migrations.AlterModelOptions(
            name='pressoutlet',
            options={'ordering': ('name',)},
        ),
    ]
