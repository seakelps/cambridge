from django.urls import re_path, include
from .views import (
    RankedListDetail,
    RankedListExplore,
    MyList,
    UpdateNote,
    delete_note,
    DownloadRankedList,
    MakePublic,
    MakeOrdered,
    append_to_ballot,
    RenameBallot,
)


urlpatterns = [
    re_path(r"^mine/(?P<year>\d+)/(?P<position>\w+)/$", view=MyList.as_view(), name="my_ranking"),
    re_path(r"^mine/append/(?P<year>\d+)/(?P<position>\w+)/(?P<slug>[-_\w]+)$", view=append_to_ballot, name="append_to_ballot"),
    re_path("^mine/rename/$", view=RenameBallot.as_view(), name="rename_ballot"),
    re_path("^mine/make-public/$", view=MakePublic.as_view(), name="make_public"),
    re_path("^mine/make-ordered/$", view=MakeOrdered.as_view(), name="make_ordered"),
    re_path(r"^notes/(?P<slug>[-_\w]+)/$", view=UpdateNote.as_view(), name="update_note"),
    re_path(r"^delete/(?P<slug>[-_\w]+)/$", view=delete_note, name="delete_note"),
    re_path(
        "^explore/",
        include(
            [
                re_path(r"^$", view=RankedListExplore.as_view(), name="list_explore"),
                re_path(
                    r"^(?P<slug>[-_\w]+)/$", view=RankedListDetail.as_view(), name="list_explore"
                ),
                re_path(
                    r"^(?P<slug>[-_\w]+)/download/$",
                    view=DownloadRankedList.as_view(),
                    name="list_explore_download",
                ),
            ]
        ),
    ),
]
