# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from pycones.reviewers.views import ReviewListView, ReviewView


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ReviewView.as_view(), name="details"),
    url(r'^$', ReviewListView.as_view(), name="list"),
]
