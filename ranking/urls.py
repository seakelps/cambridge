from django.urls import re_path, include
from .views import (
    MyList,
    UpdateNote,
    delete_note,
    MakeOrdered,
    append_to_ballot,
    RenameBallot,
)


urlpatterns = [
    re_path(r"^mine/$", view=MyList.as_view(), name="my_ranking"),
    re_path(r"^mine/append/(?P<slug>[-_\w]+)$", view=append_to_ballot, name="append_to_ballot"),
    re_path(r"^mine/rename/$", view=RenameBallot.as_view(), name="rename_ballot"),
    re_path(r"^mine/make-ordered/$", view=MakeOrdered.as_view(), name="make_ordered"),
    re_path(r"^notes/(?P<slug>[-_\w]+)/$", view=UpdateNote.as_view(), name="update_note"),
    re_path(r"^delete/(?P<slug>[-_\w]+)/$", view=delete_note, name="delete_note"),
]
