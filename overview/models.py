from django.db import models


class Candidate(models.Model):
    fullname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)

    # restricting this field
    pronoun_choices = (
        ('she',  'She'),
        ('he',   'He'),
        ('they', 'They'),
    )
    pronoun = models.CharField(max_length=4, choices=pronoun_choices)

    # the status of the candidate can be determined from these
    # two boolean fields
    is_running = models.NullBooleanField()
    is_incumbent = models.BooleanField(default=0)

    headshot = models.ImageField(default='', blank=True, upload_to='headshots/')

    def __str__(self):
        return self.fullname
