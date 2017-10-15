from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Candidate(models.Model):
    timestamp_modified = models.DateTimeField(auto_now=True)

    ##### section: campaign, free text about
    # very very basics
    slug = models.SlugField()
    fullname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)

    # what pronoun they use
    pronoun_choices = (
        ('she',  'She'),
        ('he',   'He'),
        ('they', 'They'),
    )
    pronoun = models.CharField(max_length=4, choices=pronoun_choices)

    # contact, campaign info
    email = models.EmailField(blank=True, default="")
    campaign_manager = models.CharField(max_length=200, blank=True, default="")
    website = models.URLField(help_text="Main candidate website", blank=True, default="")
    facebook = models.CharField(max_length=100, help_text="Candidate facebook page", blank=True, default="")
    twitter = models.CharField(max_length=100, blank=True, default="")

    # voting
    voter_id_number = models.CharField(max_length=100, blank=True, default="")
    date_of_registration = models.DateField(blank=True, null=True)
    voter_status_choices = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('u',  'Unknown'),
    )
    voter_status = models.CharField(max_length=3, choices=voter_status_choices, default='u', blank=True)

    # blurbs
    private_notes = models.TextField(blank=True)
    blurb = models.TextField(help_text="Text to display. Publically readable!", blank=True)

    ##### section: basic abouts
    ## electioning

    # the status of the candidate can be determined from these
    # two boolean fields
    is_running = models.NullBooleanField()
    is_incumbent = models.BooleanField(default=0)
    # number of #1 votes last election?
    # round elected in in last election?

    # political affiliation
    party_choices = (
        ('dem', 'Democrat'),
        ('rep', 'Republican'),
        ('o',   'Other'),
        ('u',   'Unknown'),
    )
    political_party = models.CharField(max_length=3, choices=party_choices, default='u', blank=True)
    # would be interesting to try to catch the active level they are

    # previous political experience?

    ## housing
    # where they live
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    housing_choices = (
        ('rent', 'Rent'),
        ('own',  'Own'),
        ('dorm', 'Dorm'),
        ('o',    'Other'),
        ('u',    'Live')
    )
    housing_status = models.CharField(max_length=4, choices=housing_choices, default='u', blank=True)
    housing_status_note = models.CharField(max_length=200, null=True, blank=True)
    housing_sell_value = models.FloatField(null=True, blank=True)
    housing_sale_date = models.DateField(null=True, blank=True)
    housing_sale_price = models.FloatField(null=True, blank=True)
    housing_sale_price_inflation = models.FloatField(null=True, blank=True)

    ## demographics
    # birth
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=200, blank=True)

    # education
    education = models.CharField(help_text="like what degrees they have", max_length=200, blank=True)

    # lifestyle
    is_cyclist = models.NullBooleanField()
    job = models.CharField(max_length=200, blank=True)

    # and more
    # race? ethnicity? lgbt?

    ##### section: interviews

    ##### section: press

    endorsements_link = models.URLField(help_text="Endorsements List", blank=True, default="")

    ##### section: finance

    # primarily for linking to finance records
    cpf_id = models.IntegerField(null=True, blank=True)
    previous_results_map = models.URLField(
        help_text="previous election results from Davi",
        blank=True, null=True)

    ##### finally, defined functions
    @cached_property
    def headshot(self):
        try:
            return staticfiles_storage.url(u'headshots/{0.slug}.png'.format(self))
        except ValueError:
            return staticfiles_storage.url(u'headshots/blank.png')
    headshot_description = models.CharField(default='headshot of candidate', max_length=500)

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("candidate_detail", args=[self.slug])

    @property
    def facebook_url(self):
        if self.facebook:
            return "https://www.facebook.com/{}/".format(self.facebook)

    @property
    def twitter_url(self):
        if self.twitter:
            return "https://twitter.com/{}".format(self.twitter)


class Organization(models.Model):
    name = models.CharField(max_length=40, unique=True)
    logo = models.URLField(blank=True, max_length=150)

    def __str__(self):
        return self.name


class Endorsement(models.Model):
    organization = models.ForeignKey(Organization)
    candidate = models.ForeignKey(Candidate)
    date = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=150, blank=True)


class Questionnaire(models.Model):
    name = models.CharField(max_length=40, unique=True)
    topic = models.CharField(max_length=40)
    icon_class = models.CharField(max_length=40, help_text='icon class like "fa-tree"')
    description = models.CharField(max_length=500)
    link = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class QuestionnaireResponse(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    candidate = models.ForeignKey(Candidate)
    date = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=250, blank=True)

    @property
    def questionnaire_link(self):
        return self.link or self.questionnaire.link

    def __str__(self):
        return "{} answering {}".format(self.candidate, self.questionnaire)


class VisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visible=True)


class InterviewVideo(models.Model):
    candidate = models.ForeignKey(Candidate)
    sort_order = models.FloatField(blank=True)
    link = models.URLField(max_length=500, blank=True)
    visible = models.BooleanField(default=True)

    objects = models.Manager()
    active = VisibleManager()

    def save(self, *args, **kwargs):
        if not self.sort_order:
            self.sort_order = InterviewVideo.objects.aggregate(models.Max('id'))['id__max']

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["sort_order"]
