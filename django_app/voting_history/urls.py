from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^full/$", views.VotingRecord.as_view(), name="full_history"),
]
