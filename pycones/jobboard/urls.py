# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from pycones.jobboard.views import JobBoardView, JobOfferView

app_name = "jobboard"

urlpatterns = [
    url(r"^(?P<pk>\d+)/$", JobOfferView.as_view(), name="details"),
    url(r"^$", JobBoardView.as_view(), name="list"),
]
