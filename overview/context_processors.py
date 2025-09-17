from django.conf import settings
from .models import Candidate, CandidateElection


def header(request):
    incumbents = CandidateElection.objects.filter(is_incumbent=True, hide=False).order_by(
        "-is_running", "candidate__fullname"
    )
    non_incumbents = CandidateElection.objects.filter(is_incumbent=False, hide=False).order_by(
        "-is_running", "candidate__fullname"
    )
    return {"incumbents": incumbents, "non_incumbents": non_incumbents}


def constants(request):
    return {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "GOOGLE_EMBED_API_KEY": settings.GOOGLE_EMBED_API_KEY,
    }
