# Generated by Django 2.2.4 on 2019-10-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0042_candidate_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questionnaireresponse',
            name='display',
            field=models.BooleanField(default=False),
        ),
    ]
