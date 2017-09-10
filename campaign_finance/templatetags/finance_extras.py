from django import template
from campaign_finance.models import get_candidate_2017_spent

register = template.Library()


# to make it easy to display some money
@register.simple_tag
def current_spend(cpf_id):
    return get_candidate_2017_spent(cpf_id)
