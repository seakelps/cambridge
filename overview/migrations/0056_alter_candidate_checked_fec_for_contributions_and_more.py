# Generated by Django 4.2.4 on 2023-08-22 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0055_auto_20211024_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='checked_fec_for_contributions',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='checked_ocpf_for_contributions',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='hide',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='housing_is_a_landlord',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='is_cyclist',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='is_running',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='candidatespecificproposalstance',
            name='simple_yes_no',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
