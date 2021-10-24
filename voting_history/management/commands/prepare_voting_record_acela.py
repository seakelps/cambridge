"""
for voting records scraped entirely from acela site
"""

import argparse
import re
import csv
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=argparse.FileType("r"), metavar="<voting-record-$date.csv>"
        )

    def handle(self, *args, csv_file, **kwargs):
        reader = csv.DictReader(csv_file)

        voting_history = []
        for row in reader:
            acela_description = row["item_body"]
            acela_description = re.sub(r"\n+\|?\n*", " ", acela_description)
            acela_description = re.sub(r" {2,}", " ", acela_description)
            acela_description = acela_description.strip()

            voting_history.append(
                {
                    "meetingid": row["meeting_id"],
                    "resolutionid": row["item_id"],
                    "aceladescription": acela_description,
                    "full_text": row["item_description"] + " " + acela_description,
                    "meetingdate": row["date"],
                    "resolutionshorttitle": row["item_description"].strip(),
                    "dennis_carlone": row["Dennis J. Carlone"],
                    "alanna_mallon": row["Alanna Mallon"],
                    "marc_mcgovern": row["Marc C. McGovern"],
                    "sumbul_siddiqui": row["Sumbul Siddiqui"],
                    "denise_simmons": row["E. Denise Simmons"],
                    "tim_toomey": row["Timothy J. Toomey"],
                    "quinton_zondervan": row["Quinton Zondervan"],
                    "jivan_sobrinho-wheeler": row["Jivan Sobrinho-Wheeler"],
                    "patty_nolan": row["Patty Nolan"],
                }
            )

        with open("static/voting_record.prepared.json", "w") as fp:
            json.dump({"data": voting_history}, fp, indent=2)
