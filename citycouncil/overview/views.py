from django.shortcuts import render

from .models import Candidate


# asdasd
def index(request):
    incumbents = Candidate.objects.filter(is_incumbent=True).order_by('fullname')
    non_incumbents = Candidate.objects.filter(is_incumbent=False).order_by('fullname')
    context = {'incumbents': incumbents, 'non_incumbents': non_incumbents}
    return render(request, 'overview/index.html', context)



# todo: detail?
