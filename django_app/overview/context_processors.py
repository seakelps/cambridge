from django.conf import settings
from .models import Election
import logging


def header(request):
    context = {}

    try:
        context["election"] = election = Election.objects.filter(
            year=request.resolver_match.kwargs["year"],
            position=request.resolver_match.kwargs["position"],
        ).first()
    except KeyError:
        # page without year / position e.g. admin view
        context["election"] = Election.objects.filter(
            year=settings.ELECTION_DATE.year,
            position="council",
        ).first()
    else:
        if election:
            candidates = election.candidate_elections.filter(hide=False).order_by("-is_running", "candidate__fullname").select_related("candidate")
            context.update({
                "incumbents": candidates.filter(is_incumbent=True),
                "non_incumbents": candidates.filter(is_incumbent=False),
            })
        else:
            logging.warning("header context: no election found")
    return context


def constants(request):
    return {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "GOOGLE_EMBED_API_KEY": settings.GOOGLE_EMBED_API_KEY,
        "ELECTION_DATE": settings.ELECTION_DATE,
        "BING_VALIDATE": settings.BING_VALIDATE,
    }
