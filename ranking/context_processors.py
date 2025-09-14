import json
from markdown import markdown

from collections import defaultdict
from overview.models import Candidate
from .models import RankedList, RankedElement


def sidebar(request):
    ranking_lookup = defaultdict(lambda: {"order": None, "comment": ""})

    ranked_list = RankedList.objects.for_request(request, force=False)
    annotated_candidates = (
        ranked_list.annotated_candidates.all() if ranked_list else RankedElement.objects.none()
    )

    for ac in annotated_candidates.all():
        ranking_lookup[ac.candidate] = {"comment": ac.comment, "order": ac.order}

    context = {
        "my_ranking": ranked_list,
        "my_candidates": [element.candidate for element in annotated_candidates],
        "runners": Candidate.objects.filter(is_running=True, hide=False),
        "runnerJson": json.dumps(
            [
                {
                    "slug": c.slug,
                    "name": c.fullname,
                    "blurb": markdown(c.blurb),
                    "img_url": c.headshot.url,
                    "img_alt": c.headshot_description,
                    "comment": ranking_lookup[c]["comment"],
                    "order": ranking_lookup[c]["order"],
                }
                for c in Candidate.objects.filter(is_running=True, hide=False)
            ]
        ),
    }

    if request.GET.get("sidebar") == "true":
        context["sidebar_visible"] = True

    return context
