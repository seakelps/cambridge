from django.conf import settings
from .models import Election
import logging


def header(request):
    try:
        election = Election.objects.filter(
            year=request.resolver_match.kwargs["year"],
            position=request.resolver_match.kwargs["position"],
        ).first()
    except KeyError:
        # page without year / position e.g. admin view
        pass
    else:
        if election:
            candidates = election.candidate_elections.filter(hide=False).order_by("-is_running", "candidate__fullname")
            return {
                "election": election,
                "incumbents": candidates.filter(is_incumbent=True),
                "non_incumbents": candidates.filter(is_incumbent=False),
            }
        else:
            logging.warning("header context: no election found")
    return {}


def constants(request):
    return {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "GOOGLE_EMBED_API_KEY": settings.GOOGLE_EMBED_API_KEY,
        "ELECTION_DATE": settings.ELECTION_DATE,
    }
