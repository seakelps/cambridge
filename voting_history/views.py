from django.views.generic import TemplateView


class VotingRecord(TemplateView):
    """ data produced by the voting_record.py script """
    template_name = "voting_history/full_history.html"
