from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^comparison/$', views.FinanceComparison.as_view(), name='finance_comparison'),
]
