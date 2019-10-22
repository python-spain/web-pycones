# -*- coding: utf-8 -*-

from django.conf.urls import url

from pycones.schedules.views import ShowSchedule, ShowSlot


app_name = "schedules"

urlpatterns = [
    url(r"^(?P<slot>.+)/$", ShowSlot.as_view(), name="slot"),
    url(r"^$", ShowSchedule.as_view(), name="show"),
]
