import os.path
import csv
import re
import json
from functools import reduce
from operator import mul
from collections import Counter

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Make voting_record.json from voting_record.csv'

    # not quite kosher, since static isn't necessarily the static_dir, but
    # we're checking it in so it doesn't matter much
    csv_source = os.path.join(settings.BASE_DIR, 'static', 'voting_record.csv')
    json_out = os.path.join(settings.BASE_DIR, 'static', 'voting_record.json')
    junk = (re.compile(regex) for regex in [
        "Transmitting Communication.*?relative to",
        "A communication was received.*?(transmitting|regarding|informing)",
        "A communication transmitted from.*?(relative to|transmitting|regarding|informing)",
        "That the City Manager.*?and to report back to the City Council on",
        "That the City Council go on record",
        r"(\ba )?grant from.*for (?=\$)",
        "relative to",
        r"Councillor [A-Z]\w*?\b",
        "the appropriation of", r"\bthe\b", r"\ba\b", r"\bof\b", r"\bfiled\b"
    ])

    def add_short_description(self, row):
        """ reduce some junk where we can from the short descriptions so the
        preview is more useful """
        short_description = row['item_description']

        for j in self.junk:
            short_description = j.sub("", short_description)

        short_description = re.sub("\s+", " ", short_description).strip(', ')

        if short_description:
            row['short_description'] = short_description[0].upper() + short_description[1:]
        else:
            row['short_description'] = ''  # js crashes otherwise

    def add_key_vote(self, row):
        """ calculate key votes based on "controversialness". hopefully
        designed to work for larger voter bases """
        vals = Counter(row[c] for c in self.candidates)
        vals.pop("Absent", "")

        # normal product runs into issues floor effects, so boosting by 10 to get
        # it favor many splits of equal size. Might be worth considering the
        # Absents if this isn't a good enough seed
        row['key_vote'] = reduce(mul, (10 + x for x in vals.values())) > len(self.candidates) + 10

    def handle(self, *args, **kwargs):
        with open("static/voting_record.csv", "r") as fp:
            reader = csv.DictReader(fp)
            rows = list(reader)

        self.candidates = reader.fieldnames[5:]

        for row in rows:
            self.add_short_description(row)
            self.add_key_vote(row)

        json.dump({"data": rows}, open("static/voting_record.json", "w"), indent=True)
