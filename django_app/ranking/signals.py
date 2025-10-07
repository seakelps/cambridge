from django.dispatch import receiver
from django_registration.signals import user_registered
from django.conf import settings
from .models import RankedList
from overview.models import Election


@receiver(user_registered)
def upgrade_anon_ranking(sender, user, request, **kwargs):
    for position in ["council", "school"]:
        election = Election.objects.get(year=settings.ELECTION_DATE.year, position=position)
        try:
            ranking = RankedList.objects.get(
                owner=None,
                election=election,
                pk=request.session[f"ranked_list_{position}_id"]
            )
        except (KeyError, RankedList.DoesNotExist):
            pass
        else:
            ranking.owner = user
            ranking.name = RankedList.make_name(user, election)
            ranking.slug = user.username
            ranking.save()
