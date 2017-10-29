from django.contrib import admin

from .models import RankedList


class RankedListAdmin(admin.ModelAdmin):
    raw_id_fields = ['owner']
    list_filer = ['public']
    date_hierarchy = 'last_modified'
    list_display = ['name', 'owner', 'last_modified', 'public']


admin.site.register(RankedList, RankedListAdmin)
