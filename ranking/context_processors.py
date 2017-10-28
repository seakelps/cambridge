import json
from markdown import markdown

from collections import defaultdict
from overview.models import Candidate
from .models import RankedList


def sidebar(request):
    ranking_lookup = defaultdict(lambda: {"order": None, "comment": ""})

    if request.user.is_authenticated:
        ranked_list = RankedList.objects.for_user(request.user)

        for ac in ranked_list.annotated_candidates.all():
            ranking_lookup[ac.candidate] = {
                "comment": ac.comment,
                "order": ac.order
            }
    else:
        ranked_list = None

    context = {
        'my_ranking': ranked_list,
        'runners': Candidate.objects.filter(is_running=True),
        'runnerJson': json.dumps([
            {
                "slug": c.slug,
                "name": c.fullname,
                "blurb": markdown(c.blurb),
                "img_url": c.headshot,
                "img_alt": c.headshot_description,
                "comment": ranking_lookup[c]["comment"],
                "order": ranking_lookup[c]["order"],
            } for c in Candidate.objects.all()])
    }

    return context
