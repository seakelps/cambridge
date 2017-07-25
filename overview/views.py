import json
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Candidate
from .utils import get_candidate_locations

from campaign_finance.models import RawBankReport
from campaign_finance.models import get_candidate_money_at_start_of_2017, get_candidate_2017_spent, get_candidate_2017_raised


# servering the jumbotron page
def index(request):
    num_runners = Candidate.objects.exclude(is_running=False).count()

    description = """
        If you want more information before you cast your 2017
        ballot for Cambridge City Council, you've come to the right place. We're
        compiling everything we can find - from op-eds to campaign finance records.
        Determine who deserves your #1 vote - or your #{num_runners}!
    """.format(num_runners=num_runners).strip()

    return render(request, 'overview/index.html', context={
        'title': "Vote Local!",
        'description': description,
        'num_runners': num_runners,
        'candidate_locations': json.dumps(list(get_candidate_locations().values())),
    })


class CandidateList(ListView):
    model = Candidate
    template_name = 'overview/candidate_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateList, self).get_context_data(*args, **kwargs)

        candidates = Candidate.objects.order_by("fullname")
        context['runners'] = candidates.exclude(is_running=False)
        context['not_runners'] = candidates.filter(is_running=False)
        return context


class CandidateDetail(DetailView):
    model = Candidate

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateDetail, self).get_context_data(*args, **kwargs)
        candidate_locations = get_candidate_locations(default_color='EEE')
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id]['color'] = 'F00'
        context['candidate_locations'] = json.dumps(list(candidate_locations.values()))

        if self.object.cpf_id:
            context['latest_bank_report'] = RawBankReport.objects.filter(cpf_id=self.object.cpf_id).latest("filing_date")
            context['money_2017_start'] = get_candidate_money_at_start_of_2017(self.object.cpf_id)
            context['money_2017_spent'] = get_candidate_2017_spent(self.object.cpf_id)
            context['money_2017_raised'] = get_candidate_2017_raised(self.object.cpf_id)
        else:
            context['latest_bank_report'] = None
            context['money_2017_start'] = None
            context['money_2017_spent'] = None
            context['money_2017_raised'] = None

        return context
