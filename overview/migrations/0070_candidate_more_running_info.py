# Generated by Django 4.2.5 on 2023-10-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0069_candidate_n_terms_in_council_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='more_running_info',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
