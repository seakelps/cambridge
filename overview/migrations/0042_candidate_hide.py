# Generated by Django 2.2.2 on 2019-07-08 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0041_auto_20171029_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='hide',
            field=models.NullBooleanField(default=0),
        ),
    ]