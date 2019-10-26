from django.dispatch import receiver
from django_registration.signals import user_registered
from .models import RankedList


@receiver(user_registered)
def upgrade_anon_ranking(sender, user, request, **kwargs):
    try:
        ranking = RankedList.objects.get(owner=None, pk=request.session['ranked_list_id'])
    except (KeyError, RankedList.DoesNotExist):
        pass
    else:
        ranking.owner = user
        ranking.name = RankedList.make_name(user)
        ranking.slug = user.username
        ranking.save()
