# Generated by Django 4.2.5 on 2023-10-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0070_candidate_more_running_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='degree',
            name='subject',
            field=models.CharField(blank=True, max_length=200, help_text='History, etc.'),
        ),
    ]
