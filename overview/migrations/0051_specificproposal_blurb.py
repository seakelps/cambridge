# Generated by Django 2.2.24 on 2021-10-24 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0050_specificproposal_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificproposal',
            name='blurb',
            field=models.TextField(blank=True),
        ),
    ]
