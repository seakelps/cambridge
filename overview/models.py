from django.db import models
from django.utils.functional import cached_property
from django.contrib.staticfiles.storage import staticfiles_storage


class Candidate(models.Model):
    slug = models.SlugField()
    fullname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # restricting this field
    pronoun_choices = (
        ('she', 'She'),
        ('he', 'He'),
        ('they', 'They'),
    )
    pronoun = models.CharField(max_length=4, choices=pronoun_choices)

    # the status of the candidate can be determined from these
    # two boolean fields
    is_running = models.NullBooleanField()
    is_incumbent = models.BooleanField(default=0)

    @cached_property
    def headshot(self):
        try:
            return staticfiles_storage.url(u'headshots/{0.slug}.png'.format(self))
        except ValueError:
            return staticfiles_storage.url(u'headshots/blank.png')
    headshot_description = models.CharField(default='headshot of candidate', max_length=500)

    def __str__(self):
        return self.fullname
