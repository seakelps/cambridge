"""citycouncil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.urls import re_path, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


class HowToVote(TemplateView):
    template_name = "how_to_vote.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = "How To Vote in Cambridge Municiple Elections"
        context['description'] = """Cambridge has a ranked choice system, which
        might be different than what you're used to. Make sure you register
        ahead of time and bring an ID with you. """
        return context


urlpatterns = [
    re_path(r'^', include('overview.urls')),
    re_path(r'^robots.txt/$', TemplateView.as_view(template_name="robots.txt"), name="robots"),
    re_path(r'^about/$', TemplateView.as_view(template_name="about_us.html"), name="about_us"),
    re_path(r'^how-to-vote/$', HowToVote.as_view(), name="how_to_vote"),
    re_path(r'^history/', include('voting_history.urls')),
    re_path(r'^finance/', include('campaign_finance.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^ranking/', include('ranking.urls')),

    # to support having users - login, logout, password management
    re_path(r'^accounts/', include('django_registration.backends.one_step.urls')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),

    # annoyed django doesn't support this by default
    re_path('^404/$', TemplateView.as_view(template_name="404.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
