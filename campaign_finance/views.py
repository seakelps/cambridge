# Holds the views for the campaign finance comparison;
# views for individual campaigns are defined in overview/views.py
from django.shortcuts import render
from django.views.generic import ListView

from campaign_finance.models import RawBankReport, ReceiptCleaned, CleanCampaignReceipt, RawCampaignReceipt
from overview.models import Candidate


class ReceiptCleaningIndex(ListView):
    model = Candidate
    template_name = 'campaign_finance/candidate_receipt_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReceiptCleaningIndex, self).get_context_data(*args, **kwargs)

        candidates = Candidate.objects.order_by("fullname")
        context['runners'] = candidates.exclude(is_running=False)
        context['not_runners'] = candidates.filter(is_running=False)
        context['title'] = "Finance cleaning"
        context['site_title'] = ""
        context['site_header'] = "Django Administration (kinda)"

        raw_receipts = RawCampaignReceipt.objects.raw('''
            select
                max(id) as id, recipient_cpf_id, count(*) as num_raw_receipts
            from
                campaign_finance_rawcampaignreceipt
            where
                id not in (
                    select raw_receipt_id
                    from campaign_finance_cleancampaignreceipt
                )
            group by
                recipient_cpf_id
        ''')

        receipt_lookup = {row.recipient_cpf_id: row.num_raw_receipts for row in raw_receipts}
        for cand in context['runners']:
            cand.num_raw_receipts = receipt_lookup.get(cand.cpf_id)

        return context
