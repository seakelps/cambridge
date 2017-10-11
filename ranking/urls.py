from django.conf.urls import url, include
from .views import RankedListDetail, RankedListExplore, MyList


urlpatterns = [
    url("^mine/$", view=MyList.as_view(), name="my_ranking"),
    url("^explore/", include([
        url(r"^$", view=RankedListExplore.as_view(), name="list_explore"),
        url(r"^(?P<slug>[-_\w]+)/$", view=RankedListDetail.as_view(), name="list_explore"),
    ])),
]
