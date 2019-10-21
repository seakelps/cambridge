import json
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Candidate
from .utils import get_candidate_locations

from campaign_finance.models import RawBankReport
from campaign_finance.models import get_candidate_money_at_start_of_2019, get_candidate_2019_spent, get_candidate_2019_raised


# servering the jumbotron page
def index(request):
    num_runners = Candidate.objects.exclude(is_running=False).exclude(hide=True).count()

    description = """
        If you want more information before you cast your 2019
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

        candidates = Candidate.objects.exclude(hide=True).order_by("fullname")
        context['runners'] = candidates.exclude(is_running=False)
        context['not_runners'] = candidates.filter(is_running=False)
        return context


class CandidateDetail(DetailView):
    model = Candidate

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateDetail, self).get_context_data(*args, **kwargs)
        context['title'] = f'Learn More About {self.object.fullname}'

        candidate_locations = get_candidate_locations(default_color='EEE')
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id].update({
                'color': 'F00',
                'main': True
            })
        context['candidate_locations'] = json.dumps(list(candidate_locations.values()))
        context['videos'] = self.object.interviewvideo_set(manager="active").all()

        context['questionnaire_responses'] = self.object.questionnaireresponse_set\
            .filter(display=True, questionnaire__display=True)\
            .select_related("questionnaire")

        context['articles'] = self.object.pressarticlecandidate_set\
            .filter(display=True)\
            .select_related("pressarticle__pressoutlet").order_by("-pressarticle__date")

        if self.object.cpf_id:
            try:
                context['latest_bank_report'] = RawBankReport.objects\
                    .filter(cpf_id=self.object.cpf_id)\
                    .latest("filing_date")
            except RawBankReport.DoesNotExist:
                context['latest_bank_report'] = None
            context['money_2019_start'] = get_candidate_money_at_start_of_2019(self.object.cpf_id)
            context['money_2019_spent'] = get_candidate_2019_spent(self.object.cpf_id)
            context['money_2019_raised'] = get_candidate_2019_raised(self.object.cpf_id)
        else:
            context['latest_bank_report'] = None
            context['money_2019_start'] = None
            context['money_2019_spent'] = None
            context['money_2019_raised'] = None

        context['endorsements'] = self.object.endorsement_set\
            .filter(display=True)\
            .select_related("organization").all()

        return context
