from overview.models import Candidate
from .models import RankedList


def sidebar(request):
    ranked_list = RankedList.objects.for_user(request.user)

    return {
        'runners': Candidate.objects.filter(is_running=True),
        'my_ranking': ranked_list,
    }
