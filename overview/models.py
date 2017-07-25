from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Candidate(models.Model):
    slug = models.SlugField()
    fullname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, default="")

    # primarily for linking to finance records
    cpf_id = models.IntegerField(null=True, blank=True)

    website = models.URLField(help_text="Main candidate website", blank=True, default="")
    facebook = models.URLField(help_text="Candidate facebook page", blank=True, default="")

    # where they live
    address = models.CharField(max_length=200, blank=True)
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

    # eh?
    party_choices = (
        ('dem', 'Democrat'),
        ('rep', 'Republican'),
        ('o', 'Other'),
        ('u', 'Unknown'),
    )
    political_party = models.CharField(max_length=3, choices=party_choices, default='u', blank=True)

    # uuuunnnstruuuucccttteeeeerrrreed
    notes = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("candidate_detail", args=[self.slug])
