"""citycouncil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', include('overview.urls')),
    url(r'^about/$', TemplateView.as_view(template_name="about_us.html"), name="about_us"),
    url(r'^votehowto/$', TemplateView.as_view(template_name="how_to_vote.html"), name="how_to_vote"),
    url(r'^compare/', include('comparison.urls')),
    url(r'^history/', include('voting_history.urls')),
    url(r'^finance/', include('campaign_finance.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
