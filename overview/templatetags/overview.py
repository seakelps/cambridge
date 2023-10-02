from markdown import markdown
from django.utils.safestring import mark_safe
from urllib.parse import urlparse

from django import template
from django.template.defaultfilters import stringfilter
from django.template.defaulttags import register


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


@register.filter(name="markdown")
@stringfilter
def md(string):
    return mark_safe(markdown(string))


@register.filter
@stringfilter
def yt_direct(video_url):
    # /embed/ link gets read as flash by facebook
    # but /v/ link is read as html5
    return video_url.replace("/embed/", "/v/")


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
