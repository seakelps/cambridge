import json

from django.views.generic import TemplateView

from overview.models import Candidate
from overview.utils import get_candidate_locations


class Compare(TemplateView):
    template_name = "comparison/compare.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Compare, self).get_context_data(*args, **kwargs)

        slugs = self.request.GET.getlist("cand")

        context['found_candidates'] = found_candidates = Candidate.objects.filter(slug__in=slugs)

        locations = get_candidate_locations(found_candidates)
        context['candidate_locations'] = json.dumps(list(locations.values()))

        found_slugs = {cand.slug for cand in found_candidates}
        context['missing_candidates'] = found_slugs.difference()
        return context
