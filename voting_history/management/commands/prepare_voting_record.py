import tqdm
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('static/voting_record.json') as fp:
            voting_history = json.load(fp)

        for row in tqdm.tqdm(voting_history):
            row['full_text'] = ' '.join(filter(None, [
                row.pop('acelatitle', ''),
                row['aceladescription'],
                row['resolutionshorttitle'],
            ]))

        with open('static/voting_record.prepared.json', 'w') as fp:
            json.dump({'data': voting_history}, fp)
