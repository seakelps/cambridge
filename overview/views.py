import json
from markdown import markdown
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse

from .models import Candidate, SpecificProposal, CandidateSpecificProposalStance
from .utils import get_candidate_locations

from campaign_finance.models import RawBankReport
from campaign_finance.models import get_candidate_money_at_start_of_2021, get_candidate_2021_spent, get_candidate_2021_raised

# servering the jumbotron page
def index(request):
    num_runners = Candidate.objects.exclude(is_running=False).exclude(hide=True).count()

    description = """
        If you want more information before you cast your 2023
        ballot for Cambridge City Council, you've come to the right place. We're
        compiling everything we can find - from op-eds to campaign finance records.
        Determine who deserves your #1, #2, or #9 vote - you've got #{num_runners} options!
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
        context['title'] = title = f'Learn More About {self.object.fullname}'
        context["description"] = description = BeautifulSoup(markdown(self.object.blurb), features='html.parser').get_text()
        context["headshot_url"] = headshot_url = self.request.build_absolute_uri(self.object.headshot)

        candidate_locations = get_candidate_locations(default_color='EEE')
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id].update({
                'color': 'F00',
                'main': True
            })
        context['candidate_locations'] = json.dumps(list(candidate_locations.values()))
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
            context['money_2021_start'] = get_candidate_money_at_start_of_2021(self.object.cpf_id)
            context['money_2021_spent'] = get_candidate_2021_spent(self.object.cpf_id)
            context['money_2021_raised'] = get_candidate_2021_raised(self.object.cpf_id)
        else:
            context['latest_bank_report'] = None
            context['money_2021_start'] = None
            context['money_2021_spent'] = None
            context['money_2021_raised'] = None

        context['endorsements'] = self.object.endorsement_set\
            .filter(display=True)\
            .select_related("organization").all()

        context["canonical_url"] = self.request.build_absolute_uri(self.object.get_absolute_url())
        context['specific_housing_support'] = self.object.candidatespecificproposalstance_set\
            .filter(display=True, specific_proposal__display=True, specific_proposal__main_topic="housing")\
            .select_related("specific_proposal").order_by("specific_proposal__order")

        context['specific_proposal_support'] = self.object.candidatespecificproposalstance_set\
            .filter(display=True, specific_proposal__display=True)\
            .exclude(specific_proposal__main_topic="housing")\
            .select_related("specific_proposal").order_by("specific_proposal__order")

        context['schema_org'] = {
            "@context": "https://schema.org",
            # "@type": "ProfilePage",  # not supported by google
            "@type": "Article",
            "name": title,
            "abstract": self.object.short_history_text,
            "description": description,
            "image": headshot_url,
            "url": self.request.build_absolute_uri(self.object.get_absolute_url()),
            "thumbnailUrl": headshot_url,
            "mainEntity": {
                "@type": "Person",
                "name": self.object.fullname,
                "birthdate": self.object.date_of_birth,
                "jobTitle": self.object.job,
                "image": headshot_url,
            }
        }

        return context


# a specific "spreadsheet-like" view of candidates' housing support
class CandidateHousingList(ListView):
    model = Candidate
    template_name = 'overview/candidates_housing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateHousingList, self).get_context_data(*args, **kwargs)

        candidates = Candidate.objects.exclude(hide=True).exclude(is_running=False).order_by("fullname")
        specific_proposals = SpecificProposal.objects.exclude(display=False).filter(main_topic="housing").order_by("order")

        candidate_specific_proposals = CandidateSpecificProposalStance.objects\
            .select_related('specific_proposal')\
            .select_related('candidate')\
            .filter(specific_proposal__display=True)\
            .filter(candidate__hide=False)\
            .filter(candidate__is_running=True)

        cp_map_yes_no = {}
        cp_map_blurb = {}

        for candidate in candidates:
            cp_map_yes_no[candidate.id] = {}
            cp_map_blurb[candidate.id] = {}

        for candidate_proposal in candidate_specific_proposals:
            cp_map_yes_no[candidate_proposal.candidate.id][candidate_proposal.specific_proposal.id] = candidate_proposal.simple_yes_no
            cp_map_blurb[candidate_proposal.candidate.id][candidate_proposal.specific_proposal.id] = candidate_proposal.blurb


        context['candidates'] = candidates
        context['specific_proposals'] = specific_proposals
        context['cp_map_yes_no'] = cp_map_yes_no
        context['cp_map_blurb'] = cp_map_blurb

        return context


class ByOrganization(TemplateView):
    template_name = "overview/by_organization.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        candidates = Candidate.objects.filter(is_running=True, hide=False)

        endorsements = {
            candidate: [
                endorsement.organization.name 
                for endorsement in candidate.endorsement_set.all()
                if endorsement.display
            ]
            for candidate in candidates.prefetch_related("endorsement_set__organization")
        }

        context["organizations"] = list(sorted(set(org_name for org_list in endorsements.values() for org_name in org_list)))

        context["endorsement_table"] = [
            [
                reverse("append_to_ballot", args=[candidate.slug]),
                candidate.fullname,
                candidate.get_absolute_url(),
                *[org_name in endorsed_orgs for org_name in context["organizations"]]
            ]
            for candidate, endorsed_orgs in endorsements.items()
        ]

        return context
