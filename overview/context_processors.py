from django.conf import settings
from .models import Election


def header(request):
    ret = {}
    for election  in Election.objects.filter(year=settings.ELECTION_DATE.year):
        ret[election.position] = {
            "incumbent" if is_incumbent else "non_incumbents": election.candidate_elections.filter(
                is_incumbent=is_incumbent, hide=False).order_by("-is_running", "candidate__fullname")
            for is_incumbent in [True, False]
        }
    print('header_context', ret)
    return ret


def constants(request):
    return {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "GOOGLE_EMBED_API_KEY": settings.GOOGLE_EMBED_API_KEY,
        "ELECTION_DATE": settings.ELECTION_DATE,
    }
