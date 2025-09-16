from django.urls import reverse
from .models import Candidate, Election, CandidateElection


def get_candidate_locations(
    candidates=CandidateElection.objects.filter(hide=False, is_running=True), default_color="F00"
):
    has_address = candidates.exclude(latitude=None).exclude(longitude=None)

    return {
        cand.id: {
            "id": cand.id,
            "name": cand.fullname,
            "lat": cand.latitude,
            "lng": cand.longitude,
            "color": default_color,
            "link": reverse("candidate_detail", args=[cand.slug]),
        }
        for cand in has_address
    }
