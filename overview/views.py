import re
import json
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

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


class VotingRecord(TemplateView):
    """ data produced by the voting_record.py script """

    def prepare_csv(self):
        import csv
        with open("static/voting_record.csv", "r") as fp:
            reader = csv.DictReader(fp)
            ll = list(reader)

        for l in ll:
            l['short_description'] = (l['item_description']
                                      .split("City Manager", 1)[-1].strip(', ')
                                      .replace("A communication was received ", "")
                                      .replace("relative to ", "")
                                      .replace("the appropriation of ", "")
                                      .replace("the ", "")  # should be word boundary
                                      .replace("a ", "")
                                      .replace("of ", ""))
            l['short_description'] = re.sub("\s+", " ", l['short_description']).strip().capitalize()

        json.dump({"data": ll}, open("static/voting_record.json", "w"), indent=True)

    template_name = "overview/voting_record.html"

    # Improve Yeas, Nays (make those columns not searchable)
    # summarize the item description more
    # move ^ to python so we only do it once
    # thumbs up thumbs down neutral clear instead of sort?
    # close the children (remove highlights? should be destroyed on reopen)
    # search body / see if we can / lemmatize and keywordify?
