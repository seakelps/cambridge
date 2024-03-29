# Generated by Django 4.2.5 on 2023-10-01 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0057_alter_pressarticle_options_alter_pressoutlet_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='overview.organization'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='year',
            field=models.IntegerField(default=2023, null=True),
        ),
    ]
