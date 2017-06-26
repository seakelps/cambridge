import json
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Candidate


# servering the jumbotron page
def index(request):
    return render(request, 'overview/index.html')


def get_candidate_locations(default_color="red"):
    has_address = Candidate.objects.exclude(latitude=None).exclude(longitude=None)

    return {cand.id: {
        'id': cand.id,
        'name': cand.fullname,
        'lat': cand.latitude,
        'lng': cand.longitude,
        'color': default_color,
    } for cand in has_address}


class CandidateList(ListView):
    model = Candidate
    template_name = 'overview/candidate_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateList, self).get_context_data(*args, **kwargs)

        candidates = Candidate.objects.order_by("fullname")
        context['runners'] = candidates.exclude(is_running=False)
        context['not_running'] = candidates.filter(is_running=False)
        context['candidate_locations'] = json.dumps(list(get_candidate_locations().values()))
        return context


class CandidateDetail(DetailView):
    model = Candidate

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateDetail, self).get_context_data(*args, **kwargs)
        candidate_locations = get_candidate_locations('wht')
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id]['color'] = 'red'
        candidate_locations[self.object.id]['color'] = 'red'
        context['candidate_locations'] = json.dumps(list(candidate_locations.values()))
        return context
