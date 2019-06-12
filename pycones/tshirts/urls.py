#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from pycones.tshirts.views import TshirtBookingView, Thanks

app_name = "tshirts"

urlpatterns = [
    url(r"^$", TshirtBookingView.as_view(), name="index"),
    url(r"^thanks/$", Thanks.as_view(), name='thanks'),
]
