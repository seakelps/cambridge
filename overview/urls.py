from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap


from . import views
from .models import Candidate


class CandidateSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Candidate.objects.all()

    def lastmod(self, obj):
        return obj.timestamp_modified


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^candidates/$', views.CandidateList.as_view(), name='all'),
    re_path(r'^candidates/(?P<slug>[-\w]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),
    re_path(r'^candidates/housing', views.CandidateHousingList.as_view(), name="housing_comparison"),
    re_path(r'^by-organization/$', views.ByOrganization.as_view(), name='by-organization'),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {
            "candidates": CandidateSitemap
        }},
        name='django.contrib.sitemaps.views.sitemap')
]
