from urllib.parse import urlparse

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def truncate_website(value):
    if value:
        parsed = urlparse(value)
        netloc = parsed.netloc.replace("www.", "")  # as short as possible
        if 'facebook' in value or 'squarespace' in value:
            return netloc + parsed.path.rstrip("/")
        else:
            return netloc

        return
    else:
        return value
