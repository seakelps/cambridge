import re
from django.contrib import admin
from django.forms import ModelForm

from .models import Candidate, Endorsement, Organization, QuestionnaireResponse, Questionnaire, InterviewVideo, PastContribution
from .models import Quote, PressOutlet, PressArticle, PressArticleCandidate


class QuestionnaireResponseInline(admin.TabularInline):
    model = QuestionnaireResponse
    autocomplete_fields = ['questionnaire']


class PastContributionInline(admin.TabularInline):
    model = PastContribution


class EndorsementInline(admin.TabularInline):
    model = Endorsement
    autocomplete_fields = ['organization']


class QuoteInline(admin.TabularInline):
    model = Quote


class PressArticleInline(admin.TabularInline):
    model = PressArticle


class PressArticleCandidateInline(admin.StackedInline):
    model = PressArticleCandidate
    autocomplete_fields = ['pressarticle']


class VideoInlineAdmin(admin.TabularInline):
    model = InterviewVideo

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

    fieldsets = [
        (None,                    {'fields': ['fullname', 'shortname', 'slug', 'pronoun', 'short_history_text']}),
        ('Campaign and Contact',  {'fields': ['email', 'campaign_manager', 'website', 'facebook', 'twitter', 'endorsements_link']}),
        ('Voting',                {'fields': ['voter_id_number', 'date_of_registration', 'voter_status']}),
        ('Our Writing',           {'fields': ['private_notes', 'blurb']}),
        ('Election',              {'fields': ['is_incumbent', 'is_running', 'hide', 'political_party', 'cpf_id']}),
        ('Housing',               {'fields': ['address', 'latitude', 'longitude', 'housing_status', 'housing_status_note', 'housing_sell_value', 'housing_sale_date', 'housing_sale_price', 'housing_sale_price_inflation']}),
        ('Demographics',          {'fields': ['date_of_birth', 'place_of_birth', 'education', 'is_cyclist', 'job', 'previous_results_map']}),
        ('Todos',                 {'fields': ['checked_ocpf_for_contributions', 'checked_fec_for_contributions']}),
    ]

    readonly_fields = ('headshot', 'has_blurb')
    list_display = ('fullname', 'is_running', 'is_incumbent', 'cpf_id', 'has_blurb')
    list_filter = ('is_running', 'is_incumbent', HasWebsite, HasBlurb, 'hide')
    prepopulated_fields = {"slug": ("fullname",)}

    inlines = [EndorsementInline, QuestionnaireResponseInline, VideoInlineAdmin, PastContributionInline, QuoteInline, PressArticleCandidateInline]

    def headshot(self, instance):
        return u"<img src='{0}' alt='{0}'>".format(instance.headshot)
    headshot.allow_tags = True

    def has_blurb(self, instance):
        return bool(instance.blurb)
    has_blurb.boolean = True


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ['has_logo']
    list_display = ('name', 'has_logo')
    inlines = [EndorsementInline]
    search_fields = ['name']

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True


class PressOutletAdmin(admin.ModelAdmin):
    readonly_fields = ['has_logo']
    list_display = ('name', 'has_logo')
    inlines = [PressArticleInline]

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True


class PressArticleAdmin(admin.ModelAdmin):
    search_fields = ['pressoutlet__name', 'title']
    inlines = [PressArticleCandidateInline]


class PastContributionAdmin(admin.ModelAdmin):
    inlines = [PastContributionInline]


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionnaireResponseInline]
    search_fields = ['name']


class QuoteAdmin(admin.ModelAdmin):
    inlines = [QuoteInline]


class PressArticleCandidateAdmin(admin.ModelAdmin):
    inlines = [PressArticleCandidateInline]


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(QuestionnaireResponse)
admin.site.register(PressOutlet, PressOutletAdmin)
admin.site.register(PressArticle, PressArticleAdmin)
