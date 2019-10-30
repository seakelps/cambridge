from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.utils import timezone

from .models import RankedList, RankedElement


class LoggedInSince(admin.SimpleListFilter):
    title = 'Seen since'
    parameter_name = 'seen_since'

    def lookups(self, request, model_admin):
        return (
            ('since', 'Has come back'),
            ('not since', 'Never came back'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset.all()
        elif self.value() == 'since':
            return queryset.filter(last_login__gt=F("date_joined") + timezone.timedelta(days=1))
        elif self.value() == 'not since':
            return queryset.exclude(last_login__gt=F("date_joined") + timezone.timedelta(days=1))
        else:
            raise ValueError(self.value())


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('date_joined', )
    list_filter = BaseUserAdmin.list_filter + (LoggedInSince, )
    date_hierarchy = 'date_joined'


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
            ('three-or-more', '3+'),
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
        elif self.value() == "three-or-more":
            return with_count.filter(count__gt=2)
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
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
