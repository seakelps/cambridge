import re
from django.contrib import admin
from django.forms import ModelForm
from django.db.models import Max, ManyToOneRel, ManyToManyRel, F

from .models import Candidate, Endorsement, Organization, QuestionnaireResponse, Questionnaire, InterviewVideo, PastContribution, Degree, CandidateVan, VanElection
from .models import Quote, PressOutlet, PressArticle, PressArticleCandidate
from .models import SpecificProposal, GeneralProposal, CandidateSpecificProposalStance, CandidateGeneralProposalStance, Forum, ForumOrganization, ForumParticipant


class QuestionnaireResponseInline(admin.TabularInline):
    model = QuestionnaireResponse
    autocomplete_fields = ['questionnaire']
    extra = 0


class PastContributionInline(admin.TabularInline):
    ordering = ("-date",)
    model = PastContribution
    extra = 0


class EndorsementInline(admin.TabularInline):
    model = Endorsement
    autocomplete_fields = ['organization']
    extra = 0


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


class PressArticleInline(admin.TabularInline):
    model = PressArticle
    extra = 0


class PressArticleCandidateInline(admin.StackedInline):
    model = PressArticleCandidate
    autocomplete_fields = ['pressarticle']
    extra = 0


class SpecificProposalInline(admin.TabularInline):
    model = SpecificProposal
    extra = 0


class CandidateSpecificProposalStanceInline(admin.StackedInline):
    model = CandidateSpecificProposalStance
    autocomplete_fields = ['specific_proposal']
    extra = 0


class GeneralProposalInline(admin.TabularInline):
    model = GeneralProposal
    extra = 0


class CandidateGeneralProposalStanceInline(admin.StackedInline):
    model = CandidateGeneralProposalStance
    autocomplete_fields = ['general_proposal']
    extra = 0


class DegreeInline(admin.TabularInline):
    model = Degree
    extra = 0


class VideoInlineAdmin(admin.TabularInline):
    model = InterviewVideo
    extra = 0

    class form(ModelForm):

        def clean_link(self):
            link = self.cleaned_data['link']

            video_match = re.match(r"^https://www.youtube.com/watch\?v=([^&]+)", link)
            if video_match:
                return "https://www.youtube.com/embed/{}".format(video_match.group(1))

            embed_match = re.match(r"^https://www.youtube.com/embed/([^&]+)", link)
            if embed_match:
                return "https://www.youtube.com/embed/{}".format(embed_match.group(1))

            vid_id_match = re.match(r"^[\w_]+$", link)
            if vid_id_match:
                return "https://www.youtube.com/embed/{}".format(vid_id_match.group())

            return link

        class Meta:
            model = InterviewVideo
            exclude = []


class HasWebsite(admin.SimpleListFilter):
    title = "Has Website"
    parameter_name = "has_website"

    def lookups(self, request, model_admin):
        return (("yes", "Yes"), ("no", "No"))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(website="")
        elif self.value() == "no":
            return queryset.filter(website="")
        else:
            return queryset


class HasBlurb(admin.SimpleListFilter):
    title = "Has Blurb"
    parameter_name = "has_blurb"

    def lookups(self, request, model_admin):
        return (("yes", "Yes"), ("no", "No"))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(blurb="")
        elif self.value() == "no":
            return queryset.filter(blurb="")
        else:
            return queryset


class CandidateAdmin(admin.ModelAdmin):
    ordering = ("hide", "-is_running", "fullname")
    fieldsets = [
        (None,                    {'fields': ['fullname', 'shortname', 'slug', 'pronoun']}),
        ('Running',               {'fields': ['short_history_text', 'n_time_running_for_council', 'n_terms_in_council', 'n_terms_on_school_committee', 'more_running_info' ]}),
        ('Campaign and Contact',  {'fields': ['email', 'van_phone', 'campaign_manager', 'website', 'facebook', 'twitter', 'linkedin', 'instagram', 'nextdoor', 'endorsements_link']}),
        ('Voting',                {'fields': ['voter_id_number', 'date_of_registration', 'voter_status', 'van_id']}),
        ('Our Writing',           {'fields': ['private_notes', 'blurb']}),
        ('Election',              {'fields': ['is_incumbent', 'is_running', 'hide', 'political_party', 'cpf_id']}),
        ('Housing - theirs',      {'fields': ['address', 'latitude', 'longitude', 'neighborhood', 'housing_status', 'housing_status_note', 'housing_sell_value', 'housing_sale_date', 'housing_sale_price', 'housing_sale_price_inflation', 'housing_type', 'housing_is_a_landlord']}),
        ('Housing - blurb',       {'fields': ['housing_private_notes', 'housing_blurb']}),
        ('Demographics',          {'fields': ['date_of_birth', 'place_of_birth', 'education', 'is_cyclist', 'job', 'previous_results_map', 'self_loan']}),
        ('Todos',                 {'fields': ['checked_ocpf_for_contributions', 'checked_fec_for_contributions']}),
    ]

    readonly_fields = ('headshot', 'has_blurb')
    list_display = (
        'fullname',
        'is_running',
        'is_incumbent',
        'cpf_id',
        'content_score',
        'related_score',
    )
    list_filter = ('is_running', 'is_incumbent', HasWebsite, HasBlurb, 'hide')
    prepopulated_fields = {"slug": ("fullname",)}

    inlines = [
        DegreeInline,
        EndorsementInline,
        CandidateSpecificProposalStanceInline,
        CandidateGeneralProposalStanceInline,
        QuestionnaireResponseInline,
        # PastContributionInline,
        QuoteInline,
        PressArticleCandidateInline,
        # VideoInlineAdmin
    ]

    def headshot(self, instance):
        return u"<img src='{0}' alt='{0}'>".format(instance.headshot)
    headshot.allow_tags = True

    @admin.display(boolean=True)
    def has_blurb(self, instance):
        return bool(instance.blurb)

    @admin.display
    def content_score(self, instance):
        missing = 0
        total = 0

        for field in instance._meta.fields:
            if field.null or field.blank:
                total += 1

                field_value = getattr(instance, field.attname)
                if field_value in (None, ""):
                    missing += 1

        return "{:.0%}".format(1 - missing / total)

    @admin.display
    def related_score(self, instance):
        missing = 0
        total = 0

        for field in instance._meta.get_fields(include_hidden=True):
            print(type(field))
            if isinstance(field, (ManyToOneRel, ManyToManyRel)):
                total += 1
                if not getattr(instance, field.get_accessor_name()).exists():
                    missing += 1

        if total > 0:
            return "{:.0%}".format(1 - missing / total)


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ['has_logo']
    list_display = ('name', 'is_local', 'is_union', 'has_logo',)
    list_filter = ('is_local', 'is_union',)
    inlines = [EndorsementInline]
    search_fields = ['name']

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True

    # def get_queryset(self, request):
    #     return Organization.objects.annotate(endorsed_on=Max())


class PressOutletAdmin(admin.ModelAdmin):
    readonly_fields = ['has_logo']
    list_display = ('name', 'has_logo')
    inlines = [PressArticleInline]

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True


class PressArticleAdmin(admin.ModelAdmin):
    ordering = [F("date").desc(nulls_last=True)]
    search_fields = ['pressoutlet__name', 'title']
    list_display = ['get_outlet', 'title', 'date']
    search_fields = ['pressoutlet__name', 'title']
    list_filter = ('pressoutlet__name', 'date',)
    inlines = [PressArticleCandidateInline]
    list_select_related = True

    def get_queryset(self, request):
        return PressArticle.objects.select_related('pressoutlet')

    def get_outlet(self, obj):
        return obj.pressoutlet.name


class PastContributionAdmin(admin.ModelAdmin):
    ordering = ("-date",)
    list_display = ['candidate', 'date', 'amount', 'recipient', 'level']
    list_filter = ('date', 'candidate',)


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionnaireResponseInline]
    ordering = ("-year", )
    search_fields = ['name']
    list_display = ['name', 'organization', 'year']
    list_filter = ('year', 'organization',)


class QuoteAdmin(admin.ModelAdmin):
    inlines = [QuoteInline]


class PressArticleCandidateAdmin(admin.ModelAdmin):
    inlines = [PressArticleCandidateInline]


class SpecificProposalAdmin(admin.ModelAdmin):
    ordering = ("display", 'main_topic', 'order')
    list_display = ['fullname', 'shortname', 'display', 'initial_year', 'main_topic', 'order']
    search_fields = ['fullname', 'shortname', 'main_topic']
    list_filter = ('initial_year', 'order',)
    inlines = [CandidateSpecificProposalStanceInline]


class GeneralProposalAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'initial_year']
    search_fields = ['fullname', 'shortname']
    inlines = [CandidateGeneralProposalStanceInline]


class CandidateVanAdminInline(admin.TabularInline):
    model = CandidateVan
    extra = 0


class VanElectionAdmin(admin.ModelAdmin):
    ordering = ("-year", "subtype")
    list_display = ['van_name', 'year', 'subtype']
    list_filter = ('year', 'subtype')
    search_fields = ['van_name', 'year', 'subtype']
    inlines = [CandidateVanAdminInline]


class CandidateVanAdmin(admin.ModelAdmin):
    ordering = ("-election__year", "candidate")
    list_display = ['candidate', 'election', 'voted', 'political_party']
    list_filter = ('voted', 'political_party', 'election',)
    search_fields = ['candidate', 'election']


class ForumOrganizationInline(admin.TabularInline):
    model = ForumOrganization
    extra = 0


class ForumParticipantInline(admin.TabularInline):
    model = ForumParticipant
    extra = 0


class ForumAdmin(admin.ModelAdmin):
    inlines = [ForumOrganizationInline, ForumParticipantInline]
    ordering = ("-year", "name")
    search_fields = ['name']
    list_display = ['name', 'date', 'year']
    list_filter = ('year',)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionnaireResponse)
admin.site.register(PressOutlet, PressOutletAdmin)
admin.site.register(PressArticle, PressArticleAdmin)
admin.site.register(SpecificProposal, SpecificProposalAdmin)
admin.site.register(GeneralProposal, GeneralProposalAdmin)
admin.site.register(PastContribution, PastContributionAdmin)
admin.site.register(VanElection,VanElectionAdmin)
admin.site.register(CandidateVan,CandidateVanAdmin)
admin.site.register(Forum, ForumAdmin)
