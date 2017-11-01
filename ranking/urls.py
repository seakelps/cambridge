from django.conf.urls import url, include
from .views import RankedListDetail, RankedListExplore, MyList, UpdateNote, delete_note


urlpatterns = [
    url("^mine/$", view=MyList.as_view(), name="my_ranking"),
    url("^notes/(?P<slug>[-_\w]+)/$", view=UpdateNote.as_view(), name="update_note"),
    url("^delete/(?P<slug>[-_\w]+)/$", view=delete_note, name="delete_note"),
    url("^explore/", include([
        url(r"^$", view=RankedListExplore.as_view(), name="list_explore"),
        url(r"^(?P<slug>[-_\w]+)/$", view=RankedListDetail.as_view(), name="list_explore"),
    ])),
]
