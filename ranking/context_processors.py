import json
from markdown import markdown

from django.conf import settings
from collections import defaultdict
from overview.models import Candidate, CandidateElection, Election
from .models import RankedList, RankedElement


def sidebar(request):
    context = {}
    ranking_lookup = defaultdict(lambda: {"order": None, "comment": ""})

    try:
        election = Election.objects.get(
            year=request.resolver_match.kwargs["year"],
            position=request.resolver_match.kwargs["position"],
        )
        ranked_list = RankedList.objects.for_request(
            request,
            election=election,
            force=False
        )
        annotated_candidates = (
            ranked_list.annotated_candidates.all() if ranked_list else RankedElement.objects.none()
        )

        for ac in annotated_candidates.all():
            ranking_lookup[ac.candidate] = {"comment": ac.comment, "order": ac.order}

        context.update({
            "my_ranking": ranked_list,
            "my_candidates": [element.candidate for element in annotated_candidates],
            "runners": CandidateElection.objects.filter(is_running=True, hide=False),
            "runnerJson": json.dumps(
                [
                    {
                        "slug": c.candidate.slug,
                        "name": c.candidate.fullname,
                        "blurb": markdown(c.blurb),
                        "img_url": c.headshot.url if c.headshot else None,
                        "img_alt": c.headshot_description,
                        "comment": ranking_lookup[c]["comment"],
                        "order": ranking_lookup[c]["order"],
                    }
                    for c in CandidateElection.objects.filter(is_running=True, hide=False).select_related("candidate")
                ]
            ),
        })

        if request.GET.get("sidebar") == "true":
            context["sidebar_visible"] = True
    except (KeyError, Election.DoesNotExist):
        pass
    return context
