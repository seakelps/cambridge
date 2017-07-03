import os.path
import csv
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Make voting_record.json from voting_record.csv'

    # not quiet cosher, since static isn't necessarily the static_dir, but
    # we're checking it in so it doesn't matter much
    csv_source = os.path.join(settings.BASE_DIR, 'static', 'voting_record.csv')
    json_out = os.path.join(settings.BASE_DIR, 'static', 'voting_record.json')

    def handle(self, *args, **kwargs):
        with open("static/voting_record.csv", "r") as fp:
            reader = csv.DictReader(fp)
            rows = list(reader)

        junk = re.compile(r'\b({})\b'.format('|'.join([
            "A communication was received", "relative to",
            "the appropriation of", "the", "a", "of"])))

        for row in rows:
            short_description = row['item_description'].split("City Manager", 1)[-1]
            short_description = junk.sub('', short_description)
            short_description = re.sub("\s+", " ", short_description).strip(', ')

            if short_description:
                row['short_description'] = short_description[0].upper() + short_description[1:]
            else:
                row['short_description'] = ''  # js crashes otherwise

        json.dump({"data": rows}, open("static/voting_record.json", "w"))
