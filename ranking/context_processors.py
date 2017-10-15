from overview.models import Candidate
from .models import RankedList


def sidebar(request):
    context = {
        'runners': Candidate.objects.filter(is_running=True),
    }

    if request.user.is_authenticated:
        ranked_list = RankedList.objects.for_user(request.user)
        context['my_ranking'] = ranked_list

    return context
