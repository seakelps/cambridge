from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^full/$', views.VotingRecord.as_view(), name='full_history'),
]
