# Holds the views for the campaign finance comparison;
# views for individual campaigns are defined in overview/views.py
from django.shortcuts import render

from .models import RawBankReport
from campaign_finance.models import (
    get_candidate_raised_year,
    get_candidate_spent_year,
    get_candidate_money_at_start_of_year,
)

from django.views.generic import TemplateView

from overview.models import Candidate



class FinanceComparison(TemplateView):
    template_name = "campaign_finance/finance_comparison.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        year = 2023

        candidates = (
            Candidate.objects.exclude(hide=True)
            .exclude(is_running=False)
            .order_by("fullname")
        )

        candidates_raised = {}
        candidates_spent = {}
        candidates_start = {}

        for c in candidates:
            candidates_raised[c.id] = get_candidate_raised_year(c.cpf_id, year)
            candidates_spent[c.id] = get_candidate_spent_year(c.cpf_id, year)
            candidates_start[c.id] = get_candidate_money_at_start_of_year(c.cpf_id, year)

        context["candidates"] = candidates
        context["candidates_raised"] = candidates_raised
        context["candidates_spent"] = candidates_spent
        context["candidates_start"] = candidates_start


        return context