from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils import timezone
from django.db.models import Sum


class Candidate(models.Model):
    """
    Holds the basic information about a political candidate.

    Historically was the "base" model, but that meant wiping
    previous years with each election.

    Should now be used only for information that is likely
    to rename relatively constant from year to year, or
    should be updated across the board when it changes.
    (ex., like name.)
    """

    class Meta:
        ordering = ("fullname",)

    def __str__(self):
        return self.fullname

    # very very basics
    slug = models.SlugField(unique=True)
    fullname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)

    # what pronoun they use
    pronoun_choices = (
        ("she", "She"),
        ("he", "He"),
        ("they", "They"),
    )
    pronoun = models.CharField(max_length=4, choices=pronoun_choices)

    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=200, blank=True)

    timestamp_modified = models.DateTimeField(auto_now=True)


class Election(models.Model):
    """
    Holds the records of elections covered.

    ex., "2025 School Committee"
    """

    def __str__(self):
        return f"{self.position} {self.year}"

    position_choices = (
        ("school", "School Committee"),
        ("council", "City Council"),
    )
    position = models.CharField(max_length=40, choices=position_choices)
    year = models.IntegerField(default=2025)


class CandidateElection(models.Model):
    """
    Mapping between candidates and elections; new "base" model
    to support historical data accuracy.

    AKA, most pieces of information on Candidate will be moving here.
    """

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_elections",
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name="candidate_elections",
    )

    # it's not pretty but it works
    short_history_text = models.CharField(max_length=200, blank=True)

    # trying to make the above more regular
    n_time_running_for_council = models.IntegerField(blank=True, null=True)
    n_terms_in_council = models.IntegerField(blank=True, null=True)
    n_terms_on_school_committee = models.IntegerField(blank=True, null=True)
    more_running_info = models.CharField(max_length=200, blank=True)

    # contact, campaign info
    email = models.EmailField(blank=True, default="")
    campaign_manager = models.CharField(max_length=200, blank=True, default="")
    website = models.URLField(help_text="Main candidate website", blank=True, default="")
    facebook = models.CharField(
        max_length=100,
        help_text="Candidate facebook page, not including facebook url",
        blank=True,
        default="",
    )
    twitter = models.CharField(
        max_length=100, blank=True, default="", help_text="twitter, not including twitter url"
    )
    bluesky = models.CharField(
        max_length=100, blank=True, default="", help_text="bluesky, not including twitter url"
    )
    linkedin = models.CharField(
        max_length=100, blank=True, default="", help_text="linkedin, not including linkedin url"
    )
    instagram = models.CharField(
        max_length=100, blank=True, default="", help_text="insta, not including instagram url"
    )
    nextdoor = models.CharField(max_length=100, blank=True, default="")

    # voting
    voter_id_number = models.CharField(max_length=100, blank=True, default="")
    date_of_registration = models.DateField(blank=True, null=True)
    voter_status_choices = (
        ("A", "Active"),
        ("I", "Inactive"),
        ("u", "Unknown"),
    )
    voter_status = models.CharField(
        max_length=3, choices=voter_status_choices, default="u", blank=True
    )
    van_id = models.CharField(max_length=50, blank=True, default="")
    van_phone = models.CharField(max_length=50, blank=True, default="")

    # blurbs
    private_notes = models.TextField(blank=True)
    blurb = models.TextField(help_text="Text to display. Publically readable!", blank=True)

    housing_private_notes = models.TextField(blank=True)
    housing_blurb = models.TextField(help_text="Text to display. Publically readable!", blank=True)

    ##### section: basic abouts
    ## electioning

    # the status of the candidate can be determined from these
    # two boolean fields
    is_running = models.BooleanField(null=True)
    is_incumbent = models.BooleanField(default=0)

    # manual hiding
    hide = models.BooleanField(default=0, null=True)

    # number of #1 votes last election?
    # round elected in in last election?

    # political affiliation
    party_choices = (
        ("dem", "Democrat"),
        ("rep", "Republican"),
        ("o", "Other"),
        ("u", "Unknown"),
    )
    political_party = models.CharField(
        max_length=3, choices=party_choices, default="u", blank=True
    )
    # would be interesting to try to catch the active level they are

    # previous political experience?

    ## housing
    # where they live
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    neighborhood = models.CharField(max_length=200, blank=True)

    housing_choices = (
        ("rent", "Rent"),
        ("own", "Own"),
        ("dorm", "Dorm"),
        ("o", "Other"),
        ("u", "Live"),
    )
    housing_status = models.CharField(
        max_length=4, choices=housing_choices, default="u", blank=True
    )
    housing_status_note = models.CharField(max_length=200, null=True, blank=True)
    housing_sell_value = models.FloatField(null=True, blank=True)
    housing_sale_date = models.DateField(null=True, blank=True)
    housing_sale_price = models.FloatField(null=True, blank=True)
    housing_sale_price_inflation = models.FloatField(null=True, blank=True)
    housing_type_choices = (
        ("single", "Single-Family"),
        ("double", "Two-Family"),
        ("triple", "Triple-Decker"),
        ("apartment", "Apartment"),
        ("dorm", "Dorm"),
        ("other", "Other"),
        ("unknown", "Unknown"),
    )
    housing_type = models.CharField(
        max_length=40, choices=housing_type_choices, default="u", blank=True
    )
    housing_is_a_landlord = models.BooleanField(null=True)

    ## demographics

    # education
    education = models.CharField(
        help_text="like what degrees they have", max_length=200, blank=True
    )

    # lifestyle
    is_cyclist = models.BooleanField(null=True)
    job = models.CharField(max_length=200, blank=True)

    # and more
    # race? ethnicity? lgbt?

    ##### section: interviews

    ##### section: press

    endorsements_link = models.URLField(help_text="Endorsements List", blank=True, default="")

    ##### section: finance

    # primarily for linking to finance records
    cpf_id = models.IntegerField(null=True, blank=True)

    # this should go somewhere else, probably
    self_loan = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    checked_ocpf_for_contributions = models.BooleanField(null=True)
    checked_fec_for_contributions = models.BooleanField(null=True)

    headshot = models.ImageField(null=True, blank=True)
    headshot_description = models.CharField(default="headshot of candidate", max_length=500)

    class Meta:
        unique_together = ("candidate", "election")

    def __str__(self):
        return f"{self.candidate.fullname} ({self.election.year} self.election.election)"

    def get_absolute_url(self):
        return reverse("candidate_detail", args=[self.election.year, self.election.position, self.candidate.slug])

    @property
    def facebook_url(self):
        if self.facebook:
            return "https://www.facebook.com/{}/".format(self.facebook)

    @property
    def twitter_url(self):
        if self.twitter:
            return "https://twitter.com/{}".format(self.twitter)

    @property
    def bluesky_url(self):
        if self.bluesky:
            return "https://bsky.app/{}".format(self.bluesky)

    @property
    def linkedin_url(self):
        if self.linkedin:
            return "https://www.linkedin.com/in/{}".format(self.linkedin)

    @property
    def instagram_url(self):
        if self.instagram:
            return "https://www.instagram.com/{}".format(self.instagram)

    @property
    def nextdoor_url(self):
        if self.nextdoor:
            return "https://nextdoor.com/profile/{}".format(self.nextdoor)

    @property
    def total_contributions_less_fees(self):
        contributions = (
            PastContribution.objects.filter(candidate=self)
            .exclude(note__contains="access fee")
            .aggregate(Sum("amount"))
        )
        return contributions["amount__sum"]

    @property
    def signed_bike_pledge(self):
        pledge = (
            Questionnaire.objects.filter(name="Cambridge Bike Safety Pledge 2023")
            .first()
            .responses.filter(candidate=self)
        )
        return pledge.exists()

    def endorsed_by_group(self, org_name):
        return self.endorsements.filter(organization__name=org_name).exists()


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True, blank=True, null=True, default=None)
    logo = models.ImageField(null=True)

    website = models.URLField(blank=True, default="")
    facebook = models.CharField(
        max_length=100,
        help_text="facebook page, not including facebook url",
        blank=True,
        default="",
    )
    twitter = models.CharField(
        max_length=100, blank=True, default="", help_text="twitter, not including twitter url"
    )
    linkedin = models.CharField(
        max_length=100, blank=True, default="", help_text="linkedin, not including linkedin url"
    )
    instagram = models.CharField(
        max_length=100, blank=True, default="", help_text="insta, not including instagram url"
    )
    reddit = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="reddit community, not including reddit url",
    )

    is_local = models.BooleanField(blank=True, default=None, null=True)
    is_union = models.BooleanField(blank=True, default=None, null=True)
    have_page = models.BooleanField(default=False)

    private_notes = models.TextField(blank=True)
    blurb = models.TextField(help_text="Text to display. Publically readable!", blank=True)

    def __str__(self):
        return self.name


class CandidateEndorsement(models.Model):
    """
    Endorsements are, naturally, per election cycle, and actually do vary
    per person/year, due to shifting votes and... drama.
    """
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="endorsements"
    )
    candidate_election = models.ForeignKey(CandidateElection, on_delete=models.CASCADE, related_name="endorsements")
    date = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=150, blank=True)
    display = models.BooleanField(default=True)

    # cambridge bike safety decided to get complicated in 2025
    note = models.CharField(max_length=100, null=True, blank=True)


class PastContribution(models.Model):
    """
    This doesn't change (but gets added to); use year to filter.
    """
    # who donated
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    # to what
    date = models.DateField(blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    # this can be complicated but we're keeping it simple for now
    recipient = models.CharField(max_length=400, null=True, blank=True)
    note = models.CharField(max_length=400, null=True, blank=True)

    # which state, federal
    level = models.CharField(max_length=4, null=True, blank=True)


class Questionnaire(models.Model):
    name = models.CharField(max_length=40, unique=True)
    topic = models.CharField(max_length=40)
    icon_class = models.CharField(max_length=40, help_text='icon class like "fa-tree"')
    organization = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.SET_NULL
    )
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="questionnaires")

    description = models.CharField(max_length=500)
    link = models.URLField(max_length=500, blank=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class QuestionnaireResponse(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="responses"
    )
    candidate_election = models.ForeignKey(CandidateElection, on_delete=models.CASCADE, related_name="responses")
    date = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=250, blank=True)
    display = models.BooleanField(default=False)

    @property
    def questionnaire_link(self):
        return self.link or self.questionnaire.link

    def __str__(self):
        return "{} answering {}".format(self.candidate, self.questionnaire)


class VisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visible=True)


class InterviewVideo(models.Model):
    """
    The first year we did this, we had enough volunteers to record our
    own videos! We haven't done that since.

    It might be nice to link to CCTV's individual interviews instead,
    or to some of the forums, especially if they're cut to particular
    candidates... not going to worry about that until later though.
    """
    candidate_election = models.ForeignKey(CandidateElection, on_delete=models.CASCADE)
    sort_order = models.FloatField(blank=True)
    link = models.URLField(max_length=500, blank=True)
    visible = models.BooleanField(default=True)

    objects = models.Manager()
    active = VisibleManager()

    def save(self, *args, **kwargs):
        if not self.sort_order:
            self.sort_order = InterviewVideo.objects.aggregate(models.Max("id"))["id__max"]

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["sort_order"]


class Quote(models.Model):
    candidate_election = models.ForeignKey(CandidateElection, on_delete=models.CASCADE)
    quote = models.TextField(help_text="Text to display. Publically readable!", blank=True)
    by = models.CharField(
        max_length=100, help_text="Leave blank if candidate", blank=True, default=""
    )
    cite = models.CharField(max_length=100, blank=True)
    display = models.BooleanField(default=False)
    display_housing = models.BooleanField(default=False)


class PressOutlet(models.Model):
    """
    ex., The Boston Globe; Cambridge Day
    """
    class Meta:
        ordering = ("name",)

    name = models.CharField(max_length=50)
    homepage = models.URLField(max_length=100, blank=True)
    logo = models.ImageField(null=True)

    def __str__(self):
        return self.name


class PressArticle(models.Model):
    """
    ex., "Record number of women running for Council"
    """
    class Meta:
        ordering = ("date",)

    pressoutlet = models.ForeignKey(PressOutlet, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    link = models.URLField(max_length=500, blank=True)
    date = models.DateField(blank=True, null=True)
    full_text = models.TextField(
        help_text="possibility to allow full text search later", blank=True, null=True
    )

    def __str__(self):
        return "{} ({})".format(self.title, self.pressoutlet)


class PressArticleCandidate(models.Model):
    """
    ex., Jan, Sumbul, Simmons, etc. mentioned in "Record number of women running"

    Right now this is remaining on candidate - might have to re-work display
    logic a bit.
    """

    pressarticle = models.ForeignKey(PressArticle, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    candidate_is_the_author = models.BooleanField(default=False)
    sample = models.TextField(
        help_text="if there's something particularly noteworthy about this candidate and press article",
        blank=True,
    )
    display = models.BooleanField(default=False)


proposal_type_choices = (
    ("housing", "Housing"),
    ("biking", "Biking"),
    ("environment", "Environment"),
    ("climate", "Climate Change"),
    ("bigotry", "Hatred/Bigotry"),
    ("governance", "Governance"),
    ("equity", "Diversity, Equity, and Inclusion"),
    ("other", "Other"),
    ("police", "Law Enforcement"),
    ("justice", "Racial Justice"),
    ("business", "Business"),
    ("education", "Education"),
    ("economy", "Jobs and Economy"),
    ("transportation", "Transportation"),
)


class Topic(models.Model):
    topic = models.CharField(max_length=200, choices=proposal_type_choices)


# ex., "AHO 2017", "AHO 2019", "MMH", "2072 Mass Ave", "Frost Terrace"
class SpecificProposal(models.Model):
    display = models.BooleanField(default=True)
    fullname = models.CharField(max_length=200, unique=True)
    shortname = models.CharField(max_length=200, blank=True)
    initial_year = models.IntegerField(null=True, blank=True)
    private_notes = models.TextField(blank=True)
    blurb = models.TextField(blank=True)
    order = models.FloatField(null=True, blank=True)

    main_topic = models.CharField(
        max_length=200, blank=True, default="", choices=proposal_type_choices
    )

    def __str__(self):
        return "{} ({})".format(self.fullname, self.initial_year)


class SpecificProposalTopic(models.Model):
    specific_proposal = models.ForeignKey(SpecificProposal, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class GeneralProposal(models.Model):
    """
    ex., "superinclusionary", "reduced parking", "no parking", etc.

    not actually sure we're using this anywhere as of 2025.
    """
    display = models.BooleanField(default=True)
    fullname = models.CharField(max_length=200, unique=True)
    shortname = models.CharField(max_length=200, blank=True)
    initial_year = models.IntegerField(null=True, blank=True)
    private_notes = models.TextField(blank=True)

    main_topic = models.CharField(
        max_length=200, blank=True, default="", choices=proposal_type_choices
    )

    def __str__(self):
        return "{} ({})".format(self.fullname, self.initial_year)


class GeneralProposalTopic(models.Model):
    specific_proposal = models.ForeignKey(GeneralProposal, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class CandidateSpecificProposalStance(models.Model):
    """
    For showing what candidates have actually been nailed down on.

    Since the specific proposals themselves are tied to years/dates,
    this is tied directly to candidates.

    ex., McGovern strongly supported the AHO v1.
    That remains as true in 2025 as it was in 2023, 2021....
    might need to re-work display logic for what election(s)
    the policies are relevant for.
    """
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    specific_proposal = models.ForeignKey(SpecificProposal, on_delete=models.CASCADE)

    display = models.BooleanField(default=True)
    simple_yes_no = models.BooleanField(default=True, null=True)
    # todo: NullBooleanField

    support_degree_choices = (
        ("supported", "Strongly Supported"),
        ("somewhat supported", "Somewhat Supported"),
        ("neither", "Neither Supported nor Opposed"),
        ("somewhat opposed", "Somewhat Opposed"),
        ("strongly opposed", "Strongly Opposed"),
        ("u", "Unknown"),
        ("na", "Not Applicable"),
        ("o", "Other"),
    )
    degree_of_support = models.CharField(
        max_length=25, choices=support_degree_choices, default="u", blank=True
    )

    # blurbs
    private_notes = models.TextField(blank=True)
    blurb = models.TextField(help_text="Text to display. Publically readable!", blank=True)


class Degree(models.Model):
    """
    Intended to simplify/ consistant-i-fy the education information of
    candidates.
    """
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="degrees")
    letters = models.CharField(max_length=200, blank=True, help_text="BA, BS, MA, etc.")
    subject = models.CharField(max_length=200, blank=True, help_text="History, etc.")
    school = models.CharField(max_length=200, blank=True, help_text="Harvard, Tufts, etc.")

    # if we need to, could use this information to only show a degree for
    # elections after the degree
    # (this avoids linking the degree to candidateelection)
    year = models.IntegerField(null=True, blank=True)


class VanElection(models.Model):
    """
    An election according to VAN/votebuilder.
    """

    # data from van
    van_name = models.CharField(max_length=100, unique=True)

    # data for us, from the above
    year = models.IntegerField(null=True, blank=True)

    subtype_choices = (
        ("general", "General"),
        ("local", "Municipal"),
        ("local_primary", "Municipal Primary"),
        ("presidental_primary", "Presidental Primary"),
        ("primary", "Primary"),
        ("special", "Special"),
        ("special_primary", "Special Primary"),
    )
    subtype = models.CharField(max_length=20, choices=subtype_choices)

    def __str__(self):
        return f"{self.van_name}: {self.year} {self.subtype}"


class CandidateVan(models.Model):
    """
    If someone voted in an election according to VAN/votebuilder.
    """

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="van_history")
    election = models.ForeignKey(
        VanElection, on_delete=models.CASCADE, related_name="candidate_map"
    )

    voted = models.BooleanField(
        blank=True,
        default=True,
        null=True,
        help_text="van/votebuilder uses various letters for how people voted; we only care that they did",
    )

    party_choices = (
        ("dem", "Democrat"),
        ("rep", "Republican"),
        ("o", "Other"),
        ("u", "Unknown"),
    )
    political_party = models.CharField(
        max_length=3, choices=party_choices, default=None, blank=True, null=True
    )

    class Meta:
        unique_together = ("candidate", "election")

    def __str__(self):
        return f"{self.candidate} {self.election}"


class Forum(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, default=2023)
    moderators = models.CharField(max_length=500, blank=True)

    description = models.CharField(max_length=500, blank=True)
    link = models.URLField(max_length=500, blank=True)
    display = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "year")

    def __str__(self):
        return f"{self.name} - {self.year}"


class ForumOrganization(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("forum", "organization")


class ForumParticipant(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="participants")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="forums")
    date = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=250, blank=True)
    display = models.BooleanField(default=True)
    timestamps = models.CharField(
        blank=True,
        max_length=100,
        help_text="list of timestamps the candidates speaks during, ex., '15:35-16:45, 1:37:02-1:38:00' ",
    )
    by_proxy = models.BooleanField(default=False)

    @property
    def forum_link(self):
        return self.link or self.forum.link

    def __str__(self):
        return f"{self.candidate} participating in {self.forum}"
