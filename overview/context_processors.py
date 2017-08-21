from django.conf import settings
from .models import Candidate


def header(request):
    incumbents = Candidate.objects.filter(is_incumbent=True).order_by('-is_running', 'fullname')
    non_incumbents = Candidate.objects.filter(is_incumbent=False).order_by('-is_running', 'fullname')
    return {'incumbents': incumbents, 'non_incumbents': non_incumbents}


def constants(request):
    return {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
    }
