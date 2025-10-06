from django import template
from campaign_finance.models import get_candidate_2019_spent

register = template.Library()


# to make it easy to display some money
@register.simple_tag
def current_spend(cpf_id):
    return get_candidate_2019_spent(cpf_id)
