"""citycouncil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.urls import path
from django.conf.urls import include, url
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
    url(r'^', include('overview.urls')),
    url(r'^about/$', TemplateView.as_view(template_name="about_us.html"), name="about_us"),
    url(r'^how-to-vote/$', HowToVote.as_view(), name="how_to_vote"),
    url(r'^history/', include('voting_history.urls')),
    url(r'^finance/', include('campaign_finance.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ranking/', include('ranking.urls')),

    # to support having users - login, logout, password management
    url(r'^accounts/', include('django_registration.backends.one_step.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
