from django.conf.urls import url, include
from .views import (
    RankedListDetail, RankedListExplore, MyList, UpdateNote, delete_note,
    DownloadRankedList, MakePublic, MakeOrdered, append_to_ballot, RenameBallot)


urlpatterns = [
    url("^mine/$", view=MyList.as_view(), name="my_ranking"),
    url(r"^mine/append/(?P<slug>[-_\w]+)$", view=append_to_ballot, name="append_to_ballot"),
    url("^mine/rename/$", view=RenameBallot.as_view(), name="rename_ballot"),
    url("^mine/make-public/$", view=MakePublic.as_view(), name="make_public"),
    url("^mine/make-ordered/$", view=MakeOrdered.as_view(), name="make_ordered"),

    url(r"^notes/(?P<slug>[-_\w]+)/$", view=UpdateNote.as_view(), name="update_note"),
    url(r"^delete/(?P<slug>[-_\w]+)/$", view=delete_note, name="delete_note"),
    url("^explore/", include([
        url(r"^$", view=RankedListExplore.as_view(), name="list_explore"),
        url(r"^(?P<slug>[-_\w]+)/$", view=RankedListDetail.as_view(), name="list_explore"),
        url(r"^(?P<slug>[-_\w]+)/download/$",
            view=DownloadRankedList.as_view(),
            name="list_explore_download"),
    ])),
]
