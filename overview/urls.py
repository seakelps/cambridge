from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidates/$', views.CandidateList.as_view(), name='all'),
    url(r'^candidates/(?P<slug>[-\w]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),
]
