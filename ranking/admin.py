from django.contrib import admin
from django.db.models import Count

from .models import RankedList, RankedElement


class CandidateInline(admin.StackedInline):
    model = RankedElement


class LengthFilter(admin.SimpleListFilter):
    """ filter ranked lists by length"""
    title = 'Length'
    parameter_name = 'length'

    def lookups(self, request, model_admin):
        return (
            ('empty', 'Empty'),
            ('non-empty', 'Non-Empty'),
            ('full', 'Full'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        with_count = queryset.annotate(count=Count("annotated_candidates"))

        if self.value() == "empty":
            return with_count.filter(count=0)
        elif self.value() == "non-empty":
            return with_count.filter(count__gt=0)
        elif self.value() == "full":
            return with_count.filter(count__gte=9)
        else:
            return with_count.all()


class RankedListAdmin(admin.ModelAdmin):
    raw_id_fields = ['owner']
    list_filter = ['public', LengthFilter]
    date_hierarchy = 'last_modified'
    list_display = ['name', 'owner', 'last_modified', 'public', 'ordered']


admin.site.register(RankedList, RankedListAdmin)
