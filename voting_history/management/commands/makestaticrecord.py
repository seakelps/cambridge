import os.path
import csv
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Make voting_record.json from voting_record.csv'

    # not quite kosher, since static isn't necessarily the static_dir, but
    # we're checking it in so it doesn't matter much
    csv_source = os.path.join(settings.BASE_DIR, 'static', 'voting_record.csv')
    json_out = os.path.join(settings.BASE_DIR, 'static', 'voting_record.json')

    def handle(self, *args, **kwargs):
        with open("static/voting_record.csv", "r") as fp:
            reader = csv.DictReader(fp)
            rows = list(reader)

        junk = [re.compile(regex) for regex in [
            "Transmitting Communication.*?relative to",
            "A communication was received.*?(transmitting|regarding|informing)",
            "A communication transmitted from.*?(relative to|transmitting|regarding|informing)",
            "That the City Manager.*?and to report back to the City Council on",
            "That the City Council go on record",
            r"(\ba )?grant from.*for (?=\$)",
            "relative to",
            r"Councillor [A-Z]\w*?\b",
            "the appropriation of", r"\bthe\b", r"\ba\b", r"\bof\b", r"\bfiled\b"
        ]]

        for row in rows:
            short_description = row['item_description']

            for j in junk:
                short_description = j.sub("", short_description)

            short_description = re.sub("\s+", " ", short_description).strip(', ')

            if short_description:
                row['short_description'] = short_description[0].upper() + short_description[1:]
            else:
                row['short_description'] = ''  # js crashes otherwise

        json.dump({"data": rows}, open("static/voting_record.json", "w"), indent=True)
