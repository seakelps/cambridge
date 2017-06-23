from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all$', views.candidate_list, name='all'),
    url(r'^candidate/(?P<slug>[-\w]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),
]
