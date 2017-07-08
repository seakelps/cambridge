from .models import Candidate


def get_candidate_locations(candidates=Candidate.objects.all(), default_color="F00"):
    has_address = Candidate.objects.exclude(latitude=None).exclude(longitude=None)

    return {cand.id: {
        'id': cand.id,
        'name': cand.fullname,
        'lat': cand.latitude,
        'lng': cand.longitude,
        'color': default_color,
    } for cand in has_address}
