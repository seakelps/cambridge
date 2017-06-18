from django.shortcuts import render
from django.db.models import Q

from .models import Candidate


# servering the jumbotron page
def index(request):
    return render(request, 'overview/index.html')


# serving the candidate overview page
def candidate_list(request):
    running = Candidate.objects.filter(Q(is_running=True) | Q(is_running=None)).order_by('fullname')
    not_running = Candidate.objects.filter(is_running=False).order_by('fullname')
    context = {'runners': running, 'not_runners': not_running}
    return render(request, 'overview/candidate_list.html', context)


# todo: detail?
