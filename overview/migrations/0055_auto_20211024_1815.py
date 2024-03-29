# Generated by Django 2.2.24 on 2021-10-24 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0054_candidate_housing_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='housing_type',
            field=models.CharField(blank=True, choices=[('single', 'Single-Family'), ('double', 'Two-Family'), ('triple', 'Triple-Decker'), ('apartment', 'Apartment'), ('dorm', 'Dorm'), ('other', 'Other'), ('unknown', 'Unknown')], default='u', max_length=40),
        ),
    ]
