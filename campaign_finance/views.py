# Holds the views for the campaign finance comparison;
# views for individual campaigns are defined in overview/views.py
from django.shortcuts import render

from .models import RawBankReport

from django.views.generic import TemplateView


class FinanceComparison(TemplateView):
    template_name = "campaign_finance/finance_comparison.html"
