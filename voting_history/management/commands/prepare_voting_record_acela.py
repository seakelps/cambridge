"""
for voting records scraped entirely from acela site
"""

import argparse
import csv
import tqdm
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=argparse.FileType("r"), metavar="<voting-record-$date.csv>")

    def handle(self, *args, csv_file, **kwargs):
        reader = csv.DictReader(csv_file)
        # meeting_id
# item_id
# date
# item_description
# item_body
# Dennis J. Carlone
# Alanna Mallon
# Marc C. McGovern
# Sumbul Siddiqui
# E. Denise Simmons
# Timothy J. Toomey
# Quinton Zondervan
# Patty Nolan
# Jivan Sobrinho-Wheeler

        voting_history = [{
            "resolutionid": row["item_id"],
            "full_text": row["item_description"] + " " + row["item_body"],
            "meetingdate": row["date"],

            "resolutionshorttitle": row["item_description"],

            "dennis_carlone": row["Dennis J. Carlone"],
            "alanna_mallon": row["Alanna Mallon"],
            "marc_mcgovern": row["Marc C. McGovern"],
            "sumbul_siddiqui": row["Sumbul Siddiqui"],
            "denise_simmons": row["E. Denise Simmons"],
            "tim_toomey": row["Timothy J. Toomey"],
            "quinton_zondervan": row["Quinton Zondervan"], 
            "jivan_sobrinho-wheeler": row["Jivan Sobrinho-Wheeler"], 
            "patty_nolan": row["Patty Nolan"], 
        } for row in reader]

        with open('static/voting_record.prepared.json', 'w') as fp:
            json.dump({'data': voting_history}, fp, indent=2)
