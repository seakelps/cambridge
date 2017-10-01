from django.contrib import admin

from .models import Candidate, Endorsement, Organization


class EndorsementInline(admin.TabularInline):
    model = Endorsement


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
        (None,                    {'fields': ['fullname', 'shortname', 'slug', 'pronoun']}),
        ('Campaign and Contact',  {'fields': ['email', 'campaign_manager', 'website', 'facebook', 'twitter']}),
        ('Voting',                {'fields': ['voter_id_number', 'date_of_registration', 'voter_status']}),
        ('Our Writing',           {'fields': ['private_notes', 'blurb']}),
        ('Election',              {'fields': ['is_incumbent', 'is_running', 'political_party']}),
        ('Housing',               {'fields': ['address', 'latitude', 'longitude', 'housing_status', 'housing_sell_value']}),
        ('Demographics',          {'fields': ['date_of_birth', 'place_of_birth', 'education', 'is_cyclist']}),
    ]

    readonly_fields = ('headshot', 'has_blurb')
    list_display = ('fullname', 'is_running', 'is_incumbent', 'cpf_id', 'has_blurb')
    list_filter = ('is_running', 'is_incumbent', HasWebsite, HasBlurb)
    prepopulated_fields = {"slug": ("fullname",)}

    inlines = [EndorsementInline]

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

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Organization, OrganizationAdmin)
