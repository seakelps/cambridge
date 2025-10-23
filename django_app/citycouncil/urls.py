"""citycouncil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.urls import re_path, include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from overview.models import Election, CandidateElection
from overview.admin import money_admin_site


class HowToVote(TemplateView):
    template_name = "how_to_vote.html"

    def get_context_data(self):
        context = super().get_context_data()
        # Doesn't really matter which one, but useful for reversing urls
        context["election"] = Election.objects.get(
            year=settings.ELECTION_DATE.year,
            position="council"
        )
        context["title"] = "How To Vote in Cambridge Municiple Elections"
        context[
            "description"
        ] = """Cambridge has a ranked choice system, which
        might be different than what you're used to. Make sure you register
        ahead of time and bring an ID with you. """
        return context


class CandidateElectionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return CandidateElection.objects.order_by('pk')

    def lastmod(self, obj):
        return obj.timestamp_modified


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return [
            reverse("about_us"),
            reverse("by-organization", args=[settings.ELECTION_DATE.year, "council"]),
            reverse("housing_comparison", args=[settings.ELECTION_DATE.year, "council"]),
            reverse("biking_comparison", args=[settings.ELECTION_DATE.year, "council"]),
            reverse("basic_comparison", args=[settings.ELECTION_DATE.year, "council"]),
            reverse("forum-list", args=[settings.ELECTION_DATE.year, "council"]),
            reverse("written-public-comment", args=[settings.ELECTION_DATE.year, "council"]),
        ]

    def location(self, item):
        return item


class Index(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("election", kwargs={
            "year": settings.ELECTION_DATE.year,
            "position": "council"
        })


urlpatterns = [
    re_path(r"^$", Index.as_view(), name="index"),
    re_path(r"^(?P<year>\d+)/(?P<position>\w+)/ranking/", include("ranking.urls")),
    re_path(r"^(?P<year>\d+)/(?P<position>\w+)/", include("overview.urls")),

    re_path(r"^robots.txt/$", TemplateView.as_view(template_name="robots.txt"), name="robots"),
    re_path(r"^about/$", TemplateView.as_view(template_name="about_us.html"), name="about_us"),
    re_path(r"^how-to-vote/$", HowToVote.as_view(), name="how_to_vote"),
    re_path(r"^history/", include("voting_history.urls")),
    re_path(r"^finance/", include("campaign_finance.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^money-admin/", money_admin_site.urls),
    # to support having users - login, logout, password management
    re_path(r"^accounts/", include("django_registration.backends.one_step.urls")),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    # annoyed django doesn't support this by default
    re_path("^404/$", TemplateView.as_view(template_name="404.html")),
    re_path("^40xxxx4/$", TemplateView.as_view(template_name="404.html")),
    # These are hosted from django since we will be using whitenoise
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),

    re_path(
        r"^sitemap\.xml$",
        sitemap,
        {
            "sitemaps": {
                "candidates": CandidateElectionSitemap,
                "static": StaticViewSitemap,
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),

]

urlpatterns += [
    # Old urls from cambridgecouncilcandidate that appear in google search results
    # this is a temporary hack to mitigate the page rank loss from changing domains
    # after ranking pretty well last cycle.
    path(
        f"candidates/{old_name}/",
        RedirectView.as_view(
            url=f"https://cambridge.vote/2025/council/candidates/{new_name}/",
            permanent=True,
        ),
    )

    for old_name, new_name in [
        ("ayah-al-zubi", "ayah-al-zubi"),
        ("ayesha-wilson", "ayesha-wilson"),
        ("burhan-azeem", "burhan-azeem"),
        ("catherine-zusy", "cathie-zusy"),
        ("denise-simmons", "e-denise-simmons"),
        ("jivan-sobrinho-wheeler", "jivan-sobrinho-wheeler"),
        ("john-hanratty", "john-hanratty"),
        ("marc-mcgovern", "marc-mcgovern"),
        ("patty-nolan", "patty-nolan"),
        ("paul-toner", "paul-toner"),
        ("peter-hsu", "peter-hsu"),
        ("robert-winters", "robert-winters"),
        ("sumbul-siddiqui", "sumbul-siddiqui"),
    ]
]


class Fix20251012(RedirectView):
    def get_redirect_url(self, year):
        return reverse("election", args=[year, "council"])


urlpatterns += [
    # Old urls from cambridge.vote, trying to capture search rank
    path(
        "topic/housing.html",
        RedirectView.as_view(
            url="/2025/council/by-topic/housing/",
            permanent=True,
        ),
    ),
    path(
        "topic/cycling.html",
        RedirectView.as_view(
            url="/2025/council/by-topic/biking/",
            permanent=True,
        ),
    ),

    # Redirect from broken link
    re_path(r"^(?P<year>\d+)/", Fix20251012.as_view()),
]
