from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^comparison/$', views.FinanceComparison.as_view(), name='finance_comparison'),
]
