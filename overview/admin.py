from django.contrib import admin

from .models import Candidate


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
    readonly_fields = ('headshot', )
    list_display = ('fullname', 'is_running', 'is_incumbent', 'cpf_id')
    list_filter = ('is_running', 'is_incumbent', HasWebsite)
    prepopulated_fields = {"slug": ("fullname",)}

    def headshot(self, instance):
        return u"<img src='{0}' alt='{0}'>".format(instance.headshot)
    headshot.allow_tags = True


admin.site.register(Candidate, CandidateAdmin)
