from .models import Candidate


def header(request):
    incumbents = Candidate.objects.filter(is_incumbent=True).order_by('fullname')
    non_incumbents = Candidate.objects.filter(is_incumbent=False).order_by('fullname')
    return {'incumbents': incumbents, 'non_incumbents': non_incumbents}
