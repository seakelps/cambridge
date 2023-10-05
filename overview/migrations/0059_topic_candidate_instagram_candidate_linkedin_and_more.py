# Generated by Django 4.2.5 on 2023-10-03 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0058_questionnaire_organization_questionnaire_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('housing', 'Housing'), ('biking', 'Biking'), ('environment', 'Environment'), ('climate', 'Climate Change'), ('bigotry', 'Hatred/Bigotry'), ('governance', 'Governance'), ('equity', 'Diversity, Equity, and Inclusion'), ('other', 'Other'), ('police', 'Law Enforcement'), ('justice', 'Racial Justice'), ('business', 'Business'), ('education', 'Education'), ('economy', 'Jobs and Economy'), ('transportation', 'Transportation')], max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='instagram',
            field=models.CharField(blank=True, default='', help_text='insta, not including instagram url', max_length=100),
        ),
        migrations.AddField(
            model_name='candidate',
            name='linkedin',
            field=models.CharField(blank=True, default='', help_text='linkedin, not including linkedin url', max_length=100),
        ),
        migrations.AddField(
            model_name='generalproposal',
            name='main_topic',
            field=models.CharField(blank=True, choices=[('housing', 'Housing'), ('biking', 'Biking'), ('environment', 'Environment'), ('climate', 'Climate Change'), ('bigotry', 'Hatred/Bigotry'), ('governance', 'Governance'), ('equity', 'Diversity, Equity, and Inclusion'), ('other', 'Other'), ('police', 'Law Enforcement'), ('justice', 'Racial Justice'), ('business', 'Business'), ('education', 'Education'), ('economy', 'Jobs and Economy'), ('transportation', 'Transportation')], default='', max_length=200),
        ),
        migrations.AddField(
            model_name='organization',
            name='blurb',
            field=models.TextField(blank=True, help_text='Text to display. Publically readable!'),
        ),
        migrations.AddField(
            model_name='organization',
            name='facebook',
            field=models.CharField(blank=True, default='', help_text='facebook page, not including facebook url', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='have_page',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='instagram',
            field=models.CharField(blank=True, default='', help_text='insta, not including instagram url', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_local',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_union',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='linkedin',
            field=models.CharField(blank=True, default='', help_text='linkedin, not including linkedin url', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='private_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='twitter',
            field=models.CharField(blank=True, default='', help_text='twitter, not including twitter url', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='specificproposal',
            name='main_topic',
            field=models.CharField(blank=True, choices=[('housing', 'Housing'), ('biking', 'Biking'), ('environment', 'Environment'), ('climate', 'Climate Change'), ('bigotry', 'Hatred/Bigotry'), ('governance', 'Governance'), ('equity', 'Diversity, Equity, and Inclusion'), ('other', 'Other'), ('police', 'Law Enforcement'), ('justice', 'Racial Justice'), ('business', 'Business'), ('education', 'Education'), ('economy', 'Jobs and Economy'), ('transportation', 'Transportation')], default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='facebook',
            field=models.CharField(blank=True, default='', help_text='Candidate facebook page, not including facebook url', max_length=100),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='twitter',
            field=models.CharField(blank=True, default='', help_text='twitter, not including twitter url', max_length=100),
        ),
        migrations.CreateModel(
            name='SpecificProposalTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specific_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.specificproposal')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.topic')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralProposalTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specific_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.generalproposal')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overview.topic')),
            ],
        ),
    ]