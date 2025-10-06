from django.urls import re_path, include

from . import views


urlpatterns = [
    re_path(r"^$", views.index, name="election"),

    re_path(r"candidates/", include([
        re_path(
            r"^$",
            views.ElectionCandidateList.as_view(),
            name="election_candidates"
        ),
        re_path(
            r"^(?P<slug>[-\w]+)/$",
            views.CandidateDetail.as_view(),
            name="candidate_detail",
        ),
    ])),

    re_path(r"by-topic/", include([
        re_path(
            r"^housing",
            views.CandidateHousingList.as_view(),
            name="housing_comparison",
        ),
        re_path(
            r"^biking/$",
            views.CandidateBikingList.as_view(),
            name="biking_comparison",
        ),
        re_path(
            r"^basic/$",
            views.CandidateBasicList.as_view(),
            name="basic_comparison",
        ),
        re_path(
            r"^forums/$",
            views.CandidateForums.as_view(),
            name="forum-list",
        ),
    ])),
    re_path(r"^by-organization/$", views.ByOrganization.as_view(), name="by-organization"),
    re_path(
        r"^written-public-comment/$",
        views.WrittenPublicComment.as_view(),
        name="written-public-comment",
    ),
]
