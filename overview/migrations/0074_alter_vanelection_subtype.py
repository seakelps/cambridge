# Generated by Django 4.2.5 on 2023-10-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0073_alter_vanelection_van_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vanelection',
            name='subtype',
            field=models.CharField(choices=[('general', 'General'), ('local', 'Municipal'), ('presidental_primary', 'Presidental Primary'), ('primary', 'Primary'), ('special', 'Special'), ('special_primary', 'Special Primary')], max_length=20),
        ),
    ]
