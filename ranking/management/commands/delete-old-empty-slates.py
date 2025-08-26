from django.core.management.base import BaseCommand, CommandError
from ranking.models import RankedList, RankedElement
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "deletes empty ranked lists that are older than 1 week old"

    def handle(self, *args, **options):

        empty_lists = (
            RankedList.objects.exclude(public=True)
            .filter(owner_id=None, annotated_candidates__isnull=True)
            .filter(last_modified__lte=datetime.now() - timedelta(days=7))
            .delete()
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully deleted %s ranked lists" % empty_lists[0])
        )
