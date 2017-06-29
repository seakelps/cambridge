from django.contrib import admin

from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    readonly_fields = ('headshot', )
    list_display = ('fullname', 'is_running', 'is_incumbent')
    list_filter = ('is_running', 'is_incumbent')
    prepopulated_fields = {"slug": ("fullname",)}

    def headshot(self, instance):
        return u"<img src='{0}' alt='{0}'>".format(instance.headshot)
    headshot.allow_tags = True


admin.site.register(Candidate, CandidateAdmin)
