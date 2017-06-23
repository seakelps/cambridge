from django.contrib import admin

from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("fullname",)}


admin.site.register(Candidate, CandidateAdmin)
