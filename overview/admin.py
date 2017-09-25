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


class CandidateAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,                    {'fields': ['fullname', 'shortname', 'slug', 'pronoun']}),
        ('Campaign and Contact',  {'fields': ['email', 'campaign_manager', 'website', 'facebook', 'twitter']}),
        ('Out Writing',           {'fields': ['private_notes', 'blurb']}),
        ('Election',              {'fields': ['is_incumbent', 'is_running', 'political_party']}),
        ('Housing',               {'fields': ['address', 'latitude', 'longitude', 'housing_status', 'housing_sell_value']}),
        ('Demographics',          {'fields': ['date_of_birth', 'place_of_birth', 'education', 'is_cyclist']}),
    ]

    readonly_fields = ('headshot', )
    list_display = ('fullname', 'is_running', 'is_incumbent', 'cpf_id')
    list_filter = ('is_running', 'is_incumbent', HasWebsite)
    prepopulated_fields = {"slug": ("fullname",)}

    inlines = [EndorsementInline]

    def headshot(self, instance):
        return u"<img src='{0}' alt='{0}'>".format(instance.headshot)
    headshot.allow_tags = True


class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ['has_logo']
    list_display = ('name', 'has_logo')
    inlines = [EndorsementInline]

    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Organization, OrganizationAdmin)
