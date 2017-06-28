from django.conf.urls import url
from . import views


urlpatterns = [
    url("^$", views.Compare.as_view(), name="compare_candidates")
]
