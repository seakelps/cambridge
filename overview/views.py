import csv
import json
import os

from bs4 import BeautifulSoup
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from markdown import markdown

from campaign_finance.models import (
    RawBankReport,
    get_candidate_raised_year,
    get_candidate_spent_year,
    get_candidate_money_at_start_of_year,
)

from .models import Candidate, Election, CandidateElection, CandidateSpecificProposalStance, Degree, SpecificProposal, Forum
from .utils import get_candidate_locations


# servering the jumbotron page
def index(request, year, position):
    election = Election.objects.get(year=year, position=position)
    num_runners = election.candidate_elections.exclude(is_running=False).exclude(hide=True).count()

    description = """
        If you want more information before you cast your {election_year}
        ballot for {position}, you've come to the right place. We're
        compiling everything we can find - from op-eds to campaign finance records.
        Determine who deserves your #1, #2, or #9 vote - you've got #{num_runners} options!
    """.format(
        election_year=settings.ELECTION_DATE.year,
        num_runners=num_runners,
        position="Cambridge City Council" if election.position == "council" else "Cambridge School Committee",
    ).strip()

    schema_org = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Cambridge Council Candidates",
        "alternateName": ["cambridge.vote"],
        "url": request.build_absolute_uri(),
    }

    return render(
        request,
        "overview/index.html",
        context={
            "title": "Vote Local!",
            "description": description,
            "num_runners": num_runners,
            "candidate_locations": json.dumps(list(get_candidate_locations().values())),
            "schema_org": schema_org,
        },
    )


class ElectionCandidateList(DetailView):
    model = Election
    template_name = "overview/candidateelection_list.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(
            year=self.kwargs["year"],
            position=self.kwargs["position"]
        )

    def get_context_data(self, *args, **kwargs):
        context = super(ElectionCandidateList, self).get_context_data(*args, **kwargs)

        candidate_elections = self.object.candidate_elections.exclude(hide=True).order_by("candidate__fullname")
        context["runners"] = candidate_elections.exclude(is_running=False)
        context["not_runners"] = candidate_elections.filter(is_running=False)
        return context


class CandidateDetail(DetailView):
    model = CandidateElection

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(
            candidate__slug=self.kwargs["slug"],
            election__year=self.kwargs["year"],
            election__position=self.kwargs["position"]
        )

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateDetail, self).get_context_data(*args, **kwargs)
        context["title"] = title = f"Learn More About {self.object.candidate.fullname}"
        context["description"] = description = BeautifulSoup(
            markdown(self.object.blurb), features="html.parser"
        ).get_text()

        candidate_locations = get_candidate_locations(default_color="EEE")
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id].update({"color": "F00", "main": True})
        context["candidate_locations"] = json.dumps(list(candidate_locations.values()))
        context["questionnaire_responses"] = self.object.responses.filter(
            display=True, questionnaire__display=True
        ).select_related("questionnaire")

        context["articles"] = (
            self.object.candidate.pressarticlecandidate_set.filter(display=True)
            .select_related("pressarticle__pressoutlet")
            .order_by("-pressarticle__date")
        )

        if self.object.cpf_id:
            try:
                context["latest_bank_report"] = RawBankReport.objects.filter(
                    cpf_id=self.object.cpf_id
                ).latest("filing_date")
            except RawBankReport.DoesNotExist:
                context["latest_bank_report"] = None

            try:
                context["money_2023_start"] = get_candidate_money_at_start_of_year(
                    self.object.cpf_id, 2023
                )
                context["money_2023_spent"] = get_candidate_spent_year(self.object.cpf_id, 2023)
                context["money_2023_raised"] = get_candidate_raised_year(self.object.cpf_id, 2023)
            except:
                context["latest_bank_report"] = None
        else:
            context["latest_bank_report"] = None
            context["money_2023_start"] = None
            context["money_2023_spent"] = None
            context["money_2023_raised"] = None

        context["endorsements"] = (
            self.object.endorsements.filter(display=True).select_related("organization").all()
        )

        context["canonical_url"] = self.request.build_absolute_uri(self.object.get_absolute_url())
        context["specific_housing_support"] = (
            self.object.candidate.candidatespecificproposalstance_set.filter(
                display=True,
                specific_proposal__display=True,
                specific_proposal__main_topic="housing",
            )
            .select_related("specific_proposal")
            .order_by("specific_proposal__order")
        )

        context["specific_proposal_support"] = (
            self.object.candidate.candidatespecificproposalstance_set.filter(
                display=True, specific_proposal__display=True
            )
            .exclude(specific_proposal__main_topic="housing")
            .select_related("specific_proposal")
            .order_by("specific_proposal__order")
        )

        context["candidate_degrees"] = self.object.candidate.degrees.all()

        context["candidate_voting_history"] = self.object.candidate.van_history.order_by(
            "-election__year"
        ).all()

        context["candidate_forums"] = (
            self.object.candidate.forums.filter(
                display=True,
                forum__display=True,
            ).select_related("forum")
            # .prefetch_related("forum__organization")
            .order_by("forum__date")
        )

        context["schema_org"] = {
            "@context": "https://schema.org",
            # "@type": "ProfilePage",  # not supported by google
            "@type": "Article",
            "name": title,
            "abstract": self.object.short_history_text,
            "description": description,
            "image": self.object.headshot.url,
            "url": self.request.build_absolute_uri(self.object.get_absolute_url()),
            "thumbnailUrl": self.object.headshot.url,
            "mainEntity": {
                "@type": "Person",
                "name": self.object.candidate.fullname,
                "birthdate": self.object.candidate.date_of_birth,
                "jobTitle": self.object.job,
                "image": self.object.headshot.url,
            },
        }

        return context


# a specific "spreadsheet-like" view of candidates' housing support
class CandidateHousingList(ListView):
    model = Candidate
    template_name = "overview/candidates_housing.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateHousingList, self).get_context_data(*args, **kwargs)

        candidates = (
            Candidate.objects.exclude(hide=True).exclude(is_running=False).order_by("fullname")
        )
        specific_proposals = (
            SpecificProposal.objects.exclude(display=False)
            .filter(main_topic="housing")
            .order_by("order")
        )

        candidate_specific_proposals = (
            CandidateSpecificProposalStance.objects.select_related("specific_proposal")
            .select_related("candidate")
            .filter(specific_proposal__display=True)
            .filter(candidate__hide=False)
            .filter(candidate__is_running=True)
        )

        cp_map_yes_no = {}
        cp_map_blurb = {}

        for candidate in candidates:
            cp_map_yes_no[candidate.id] = {}
            cp_map_blurb[candidate.id] = {}

        for candidate_proposal in candidate_specific_proposals:
            cp_map_yes_no[candidate_proposal.candidate.id][
                candidate_proposal.specific_proposal.id
            ] = candidate_proposal.simple_yes_no
            cp_map_blurb[candidate_proposal.candidate.id][
                candidate_proposal.specific_proposal.id
            ] = candidate_proposal.blurb

        context["candidates"] = candidates
        context["specific_proposals"] = specific_proposals
        context["cp_map_yes_no"] = cp_map_yes_no
        context["cp_map_blurb"] = cp_map_blurb

        return context


# a specific "spreadsheet-like" view of candidates' biking support
class CandidateBikingList(ListView):
    model = Candidate
    template_name = "overview/candidates_biking.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateBikingList, self).get_context_data(*args, **kwargs)

        candidates = (
            Candidate.objects.exclude(hide=True).exclude(is_running=False).order_by("fullname")
        )
        specific_proposals = (
            SpecificProposal.objects.exclude(display=False)
            .filter(main_topic="biking")
            .order_by("order")
        )

        candidate_specific_proposals = (
            CandidateSpecificProposalStance.objects.select_related("specific_proposal")
            .select_related("candidate")
            .filter(specific_proposal__display=True)
            .filter(candidate__hide=False)
            .filter(candidate__is_running=True)
        )

        cp_map_yes_no = {}
        cp_map_blurb = {}

        for candidate in candidates:
            cp_map_yes_no[candidate.id] = {}
            cp_map_blurb[candidate.id] = {}

        for candidate_proposal in candidate_specific_proposals:
            cp_map_yes_no[candidate_proposal.candidate.id][
                candidate_proposal.specific_proposal.id
            ] = candidate_proposal.simple_yes_no
            cp_map_blurb[candidate_proposal.candidate.id][
                candidate_proposal.specific_proposal.id
            ] = candidate_proposal.blurb

        bike_group_yes_no = {}
        mass_ave_group_yes_no = {}
        for candidate in candidates:
            bike_group_yes_no[candidate.id] = candidate.endorsed_by_group(
                "Cambridge Bicycle Safety"
            )
            mass_ave_group_yes_no[candidate.id] = candidate.endorsed_by_group("Save Mass Ave")

        context["candidates"] = candidates
        context["specific_proposals"] = specific_proposals
        context["cp_map_yes_no"] = cp_map_yes_no
        context["cp_map_blurb"] = cp_map_blurb
        context["candidate_bike_group_map"] = bike_group_yes_no
        context["candidate_mass_group_map"] = mass_ave_group_yes_no

        return context


# a specific "spreadsheet-like" view of candidate basic info
class CandidateBasicList(ListView):
    model = Candidate
    template_name = "overview/candidates_basic.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateBasicList, self).get_context_data(*args, **kwargs)

        candidates = (
            Candidate.objects.exclude(hide=True)
            .exclude(is_running=False)
            .order_by("fullname")
            .prefetch_related("degrees")
        )

        candidate_degree_map = {}
        for candidate in candidates:
            candidate_degree_map[candidate.id] = candidate.degrees.all()

        context["candidates"] = candidates
        context["candidate_degree_map"] = candidate_degree_map

        return context


class ByOrganization(TemplateView):
    template_name = "overview/by_organization.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        candidates = Candidate.objects.filter(is_running=True, hide=False)

        endorsements = {
            candidate: [
                endorsement.organization
                for endorsement in candidate.endorsements.all()
                if endorsement.display
            ]
            for candidate in candidates.prefetch_related("endorsements__organization")
        }

        # extre column for "Any Union" handled in html
        context["organizations"] = list(
            sorted(
                set(org for org_list in endorsements.values() for org in org_list),
                key=lambda o: o.name,
            )
        )

        context["endorsement_table"] = [
            [
                reverse("append_to_ballot", args=[candidate.slug]),
                candidate.fullname,
                candidate.get_absolute_url(),
                any(org.is_union for org in endorsed_orgs),
                *[org in endorsed_orgs for org in context["organizations"]],
            ]
            for candidate, endorsed_orgs in endorsements.items()
        ]
        return context


class WrittenPublicComment(TemplateView):
    template_name = "overview/candidates_public_comment.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        absolute_path = os.path.dirname(__file__)
        full_path = os.path.join(absolute_path, "public_comment.csv")
        with open(full_path, "r") as fp:
            reader = csv.reader(fp)
            context["public_comments"] = list(reader)

        return context


class CandidateForums(TemplateView):
    template_name = "overview/candidates_forums.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["candidates"] = candidates = Candidate.objects.filter(is_running=True, hide=False)
        context["forums"] = forums = Forum.objects.filter(display=True)

        dataset = {}
        for candidate in candidates:
            forum_participation = {p.forum_id: p for p in candidate.forums.all()}
            dataset[candidate] = [forum_participation.get(forum.id) for forum in forums]

        context["dataset"] = dataset

        return context
