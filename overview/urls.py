from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


from . import views
from .models import Candidate


class CandidateSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Candidate.objects.all()

    def lastmod(self, obj):
        return obj.timestamp_modified


class StaticViewSitemap(Sitemap):
    changefreq = "weeklyn"
    priority = 0.4

    def items(self):
        return [
            reverse("about_us"),
            reverse("by-organization"),
            reverse("housing_comparison"),
        ]

    def location(self, item):
        return item


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^candidates/$', views.CandidateList.as_view(), name='all'),
    re_path(r'^candidates/(?P<slug>[-\w]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),
    re_path(r'^candidates/housing', views.CandidateHousingList.as_view(), name="housing_comparison"),
    re_path(r'^by-topic/biking/$', views.CandidateBikingList.as_view(), name="biking_comparison"),
    re_path(r'^by-topic/basic/$', views.CandidateBasicList.as_view(), name="basic_comparison"),
    re_path(r'^by-organization/$', views.ByOrganization.as_view(), name='by-organization'),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {
            "candidates": CandidateSitemap,
            "static": StaticViewSitemap,
        }},
        name='django.contrib.sitemaps.views.sitemap')
]
