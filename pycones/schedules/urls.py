# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from pycones.schedules.views import ShowSchedule, ShowSlot, EditPresentation

urlpatterns = [
    url(r'^presentations/(?P<presentation_id>.+)/$', EditPresentation.as_view(), name="edit-presentation"),
    url(r'^(?P<slot>.+)/$', ShowSlot.as_view(), name="slot"),
    url(r'^$', ShowSchedule.as_view(), name="show"),
]
