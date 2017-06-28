import json
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Candidate
from .utils import get_candidate_locations


# servering the jumbotron page
def index(request):
    return render(request, 'overview/index.html')


class CandidateList(ListView):
    model = Candidate
    template_name = 'overview/candidate_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateList, self).get_context_data(*args, **kwargs)

        candidates = Candidate.objects.order_by("fullname")
        context['runners'] = candidates.exclude(is_running=False)
        context['not_runners'] = candidates.filter(is_running=False)
        return context


class CandidateDetail(DetailView):
    model = Candidate

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateDetail, self).get_context_data(*args, **kwargs)
        candidate_locations = get_candidate_locations(default_color='wht')
        # </script> will make us sad still
        if self.object.id in candidate_locations:
            candidate_locations[self.object.id]['color'] = 'red'
        context['candidate_locations'] = json.dumps(list(candidate_locations.values()))
        return context
