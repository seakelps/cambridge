from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ReceiptCleaningIndex.as_view(), name='receipt_list'),
]
