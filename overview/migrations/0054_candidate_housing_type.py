# Generated by Django 2.2.24 on 2021-10-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0053_candidate_housing_is_a_landlord'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='housing_type',
            field=models.CharField(blank=True, choices=[('single', 'Single-Family'), ('double', 'Duplex'), ('triple', 'Triple-Decker'), ('appartment', 'Appartment'), ('dorm', 'Dorm'), ('other', 'Other'), ('unknown', 'Unknown')], default='u', max_length=40),
        ),
    ]