from django.urls import reverse
from .models import Candidate, Election, CandidateElection


def get_candidate_locations(election, default_color="#F00"):
    candidates = election.candidate_elections.filter(
        hide=False,
        is_running=True
    ).select_related("candidate")

    return {
        cand.id: {
            "id": cand.id,
            "name": cand.candidate.fullname,
            "lat": cand.latitude,
            "lng": cand.longitude,
            "color": default_color,
            "link": reverse("candidate_detail", args=[election.year, election.position, cand.candidate.slug]),
        }
        for cand in candidates
    }
