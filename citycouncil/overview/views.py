from django.shortcuts import render
from django.db.models import Q

from .models import Candidate


# servering the jumbotron page
def index(request):
    incumbents = Candidate.objects.filter(is_incumbent=True).order_by('fullname')
    non_incumbents = Candidate.objects.filter(is_incumbent=False).order_by('fullname')
    context = {'incumbents': incumbents, 'non_incumbents': non_incumbents}
    return render(request, 'overview/index.html', context)


# serving the candidate overview page
def candidate_list(request):
    running = Candidate.objects.filter(Q(is_running=True) | Q(is_running=None)).order_by('fullname')
    not_running = Candidate.objects.filter(is_running=False).order_by('fullname')
    context = {'runners': running, 'not_runners': not_running}
    return render(request, 'overview/candidate_list.html', context)


# todo: detail?
