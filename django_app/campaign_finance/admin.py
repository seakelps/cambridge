from django.contrib import admin
from .models import RawBankReport


class RawBankReportAdmin(admin.ModelAdmin):
    list_display = ("ocpf_id", "cpf_id", "full_name_reverse", "report_year")

    list_filter = ("report_year",)


admin.site.register(RawBankReport, RawBankReportAdmin)
