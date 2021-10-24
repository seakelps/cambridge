# Generated by Django 2.2.24 on 2021-10-24 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0046_auto_20210810_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField(default=True)),
                ('fullname', models.CharField(max_length=200, unique=True)),
                ('shortname', models.CharField(max_length=200)),
                ('initial_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecificProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField(default=True)),
                ('fullname', models.CharField(max_length=200, unique=True)),
                ('shortname', models.CharField(max_length=200)),
                ('initial_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='housing_blurb',
            field=models.TextField(blank=True, help_text='Text to display. Publically readable!'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='housing_private_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='quote',
            name='display_housing',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CandidateSpecificProposalStance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField(default=True)),
                ('simple_yes_no', models.BooleanField(default=True)),
                ('degree_of_support', models.CharField(blank=True, choices=[('supported', 'Strongly Supported'), ('somewhat supported', 'Somewhat Supported'), ('neither', 'Neither Supported nor Opposed'), ('somewhat opposed', 'Somewhat Opposed'), ('strongly opposed', 'Strongly Opposed'), ('u', 'Unknown'), ('na', 'Not Applicable'), ('o', 'Other')], default='u', max_length=25)),
                ('private_notes', models.TextField(blank=True)),
                ('blurb', models.TextField(blank=True, help_text='Text to display. Publically readable!')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate')),
                ('specific_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.SpecificProposal')),
            ],
        ),
        migrations.CreateModel(
            name='CandidateGeneralProposalStance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField(default=True)),
                ('simple_yes_no', models.BooleanField(default=True)),
                ('private_notes', models.TextField(blank=True)),
                ('blurb', models.TextField(blank=True, help_text='Text to display. Publically readable!')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.Candidate')),
                ('general_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.GeneralProposal')),
            ],
        ),
    ]
