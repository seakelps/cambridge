# Generated by Django 2.2.24 on 2021-10-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0051_specificproposal_blurb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatespecificproposalstance',
            name='simple_yes_no',
            field=models.NullBooleanField(default=True),
        ),
    ]
