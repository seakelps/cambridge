from django.conf.urls import url
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
    url(r'^$', views.index, name='index'),
    url(r'^candidates/$', views.CandidateList.as_view(), name='all'),
    url(r'^candidates/(?P<slug>[-\w]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {
            "candidates": CandidateSitemap
        }},
        name='django.contrib.sitemaps.views.sitemap')
]
